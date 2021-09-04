from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import *
from fastapi.logger import logger

def get_transpose_df(df, columns, pivotCol):
    columnsValue = list(map(lambda x: str("'") + str(x) + str("',")  + str(x), columns))
    stackCols = ','.join(x for x in columnsValue)
    df_1 = df.selectExpr(pivotCol, "stack(" + str(len(columns)) + "," + stackCols + ")")\
           .select(pivotCol, "col0", "col1")
    final_df = df_1.groupBy(col("col0")).pivot(pivotCol).agg(concat_ws("", collect_list(col("col1"))))\
                 .withColumnRenamed("col0", pivotCol)
    return final_df

def create_feature_summary(spark, features_df):
    distict_count_summary_col = lit("distinct_count").alias("summary")
    missing_count_summary_col = lit("missing_count").alias("summary")
    exprs = [distict_count_summary_col] + [countDistinct(x).alias(x) for x in features_df.columns]

    data ={'summary':'data_type'}
    data.update( {m[0]:m[1] for m in features_df.dtypes})


    distinct_count_df = features_df.agg(*exprs)
    missing_df = features_df.select([missing_count_summary_col] +
                       [count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in features_df.columns])
    dtype_df = spark.createDataFrame([data])

    custom_summary_df = dtype_df.unionByName(missing_df).unionByName(distinct_count_df)

    summary_t_df = features_df.describe().unionByName(features_df.summary("25%", "50%", "75%")).unionByName(custom_summary_df)
    summary_df = get_transpose_df(summary_t_df, features_df.columns, "summary").withColumnRenamed("25%", "top_25"
                                ).withColumnRenamed("50%", "top_50"
                                                   ).withColumnRenamed("75%", "top_75")
    return summary_df

def read_and_process_tabular_data(data_path, keyspace, file_store="local"):
    table_name = data_path.split("/")[-1].split(".")[0]
    if file_store=="local":
        file_path_with_store = "file://" + data_path
    else:
        file_path_with_store = data_path
    summary_table_name = table_name + "_summary"
    spark = SparkSession.builder.appName("tabular_data_processing").getOrCreate()
    spark.conf.set("spark.sql.catalog.myCatalog", "com.datastax.spark.connector.datasource.CassandraCatalog")

    features_df = spark.read.option("inferSchema", "true").csv(
        file_path_with_store,
        header=True)

    summary_df = create_feature_summary(spark, features_df)
    summary_df.write.mode("append").partitionBy("summary").saveAsTable(
        "myCatalog." + keyspace + "." + summary_table_name)
    try:
        partition_key = summary_df.filter(col("distinct_count") == lit(features_df.count())).select(
            "summary").toPandas().values[0][0]
    except IndexError or KeyError:
        features_df = features_df.select("*").withColumn("partition_key_id", monotonically_increasing_id())
        partition_key= "partition_key_id"
    features_df.write.mode("append").partitionBy(partition_key).saveAsTable("myCatalog."+keyspace+"."+table_name)
    spark.stop()
    logger.info("summary table created in astra " + summary_table_name)
    return features_df.dtypes