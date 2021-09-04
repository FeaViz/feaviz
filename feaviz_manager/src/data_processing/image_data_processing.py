import cv2
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import numpy as np
from fastapi.logger import logger


def get_desc(img, network, labels, threshold, probability_minimum):
    image = cv2.imread(img.split('//')[-1])
    image_input_shape = image.shape
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    layers_names_all = network.getLayerNames()
    layers_names_output = [layers_names_all[i[0] - 1] for i in network.getUnconnectedOutLayers()]
    network.setInput(blob)  # setting blob as input to the network
    output_from_network = network.forward(layers_names_output)
    h, w = image_input_shape[:2]
    bounding_boxes = []
    confidences = []
    class_numbers = []
    class_labels = []
    for result in output_from_network:
        for detection in result:
            scores = detection[5:]
            class_current = np.argmax(scores)
            # Getting confidence (probability) for current object
            confidence_current = scores[class_current]
            # Eliminating weak predictions by minimum probability
            if confidence_current > probability_minimum:
                # Scaling bounding box coordinates to the initial image size
                # YOLO data format keeps center of detected box and its width and height
                # That is why we can just elementwise multiply them to the width and height of the image
                box_current = detection[0:4] * np.array([w, h, w, h])
                # From current box with YOLO format getting top left corner coordinates
                # that are x_min and y_min
                x_center, y_center, box_width, box_height = box_current.astype('int')
                x_min = int(x_center - (box_width / 2))
                y_min = int(y_center - (box_height / 2))
                # Adding results into prepared lists
                bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
                confidences.append(float(confidence_current))
                class_numbers.append(int(class_current))
                class_labels.append(labels[class_current])
    return Row(#"bounding_box",
               "confidence_score",
               "class",
               "class_labels")(#bounding_boxes,
                               confidences,
                               class_numbers,
                               class_labels)

def read_and_process_data(images_data_path, keyspace, http_server_url,
                                    model_label_path, model_weights_path,
                                    model_cfg_path):
    probability_minimum = 0.7

    # Setting threshold for non maximum suppression
    threshold = 0.5

    # Opening file, reading, eliminating whitespaces, and splitting by '\n', which in turn creates list
    labels = open(model_label_path).read().strip().split('\n')  # list of names

    network = cv2.dnn.readNetFromDarknet(model_cfg_path, model_weights_path)
    image_features_table_name = images_data_path.split("/")[-1]

    spark = SparkSession.builder.appName("image_processing").getOrCreate()
    spark.conf.set("spark.sql.catalog.myCatalog", "com.datastax.spark.connector.datasource.CassandraCatalog")

    img_features_df = spark.read.format("image") \
        .option("basePath", images_data_path) \
        .option("dropInvalid", True).load("file://" + images_data_path + "/*")

    schema_added = StructType([
        #     StructField("bounding_box", ArrayType(ArrayType(IntegerType())), False),
        StructField("confidence_score", ArrayType(FloatType()), False),
        StructField("classes", ArrayType(IntegerType()), False),
        StructField("class_labels", ArrayType(StringType()), False)
    ])

    udf_image = udf(lambda x: get_desc(x, network, labels, threshold, probability_minimum), schema_added)

    features_df = img_features_df.select("image.origin", "image.height", "image.width", "image.nChannels", "image.mode") \
        .withColumnRenamed("origin", "image_path")
    features_df = features_df.withColumn("desc", udf_image("image_path")).select("*", "desc.*").drop("desc")  # .show()
    image_features_df = features_df.withColumn("image_view", concat(lit('<img src="' + http_server_url),
                                                                    split(col("image_path"), images_data_path).getItem(1),
                                                                    lit('"  width="150" height="200">')))
    image_features_df.write.mode("append").partitionBy("image_path").saveAsTable(
        "myCatalog."+ keyspace +"."+ image_features_table_name)
    spark.stop()
    logger.info("Image features data written to table "+image_features_table_name)
    return 1