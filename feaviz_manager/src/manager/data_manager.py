from src.data_processing.image_data_processing import read_and_process_data
from src.data_processing.tabular_data_processing import read_and_process_tabular_data


def create_tablular_data_visualization(data_path, keyspace):
    column_dtypes_list = read_and_process_tabular_data(data_path, keyspace)
    # need to add right value here
    return 13


def create_image_data_visualization(images_data_path, keyspace, http_server_url,
                                    model_label_path, model_weights_path,
                                    model_cfg_path):
    column_dtypes_list = read_and_process_data(images_data_path, keyspace, http_server_url,
                              model_label_path, model_weights_path,
                              model_cfg_path)
    # need to add right value here
    return 12