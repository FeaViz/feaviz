from src.data_processing.image_data_processing import read_and_process_data
from src.data_processing.tabular_data_processing import read_and_process_tabular_data


def create_tablular_data_visualization(data_path, keyspace):
    return read_and_process_tabular_data(data_path, keyspace)

def create_image_data_visualization(images_data_path, keyspace, http_server_url,
                                    model_label_path, model_weights_path,
                                    model_cfg_path):
        return read_and_process_data(images_data_path, keyspace, http_server_url,
                              model_label_path, model_weights_path,
                              model_cfg_path)