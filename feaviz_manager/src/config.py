from pydantic import BaseSettings


class Settings(BaseSettings):
    http_server_url: str = "http://localhost:9753"
    keyspace = "nosql1"

    model_label_path: str = "/Users/lavanyamk/Documents/FeaViz/coco-yolo-v3/coco.names"
    model_weights_path: str = "/Users/lavanyamk/Documents/FeaViz/coco-yolo-v3/yolov3.weights"
    model_cfg_path: str = "/Users/lavanyamk/Documents/FeaViz/coco-yolo-v3/yolov3.cfg"


settings = Settings()