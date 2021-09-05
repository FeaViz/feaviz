from src.data_processing.image_data_processing import read_and_process_data
from src.data_processing.tabular_data_processing import read_and_process_tabular_data

dashboards = {"tabular_dashboard": ["http://localhost:8088/r/2", "http://localhost:8088/r/3"], "image_dashboard": "http://localhost:8088/r/7"}
def create_tablular_data_visualization(data_path, keyspace):
    column_dtypes_list = read_and_process_tabular_data(data_path, keyspace)
    # need to add right value here
    return dashboards["tabular_dashboard"]


def create_image_data_visualization(images_data_path, keyspace, http_server_url,
                                    model_label_path, model_weights_path,
                                    model_cfg_path):
    column_dtypes_list = read_and_process_data(images_data_path, keyspace, http_server_url,
                              model_label_path, model_weights_path,
                              model_cfg_path)
    # need to add right value here
    return dashboards["image_dashboard"]
