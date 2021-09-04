from .data_processing.image_data_processing import read_and_process_data
from .data_processing.tabular_data_processing import read_and_process_tabular_data


def create_tablular_data_visualization(table_name, keyspace):
    try:
        read_and_process_tabular_data(table_name, keyspace)
        return 1
    except:
        return 0

def create_image_data_visualization(images_data_path, keyspace, http_server_url,
                                    model_label_path, model_weights_path,
                                    model_cfg_path):
    try:
        read_and_process_data(images_data_path, keyspace, http_server_url,
                              model_label_path, model_weights_path,
                              model_cfg_path)

    return 1