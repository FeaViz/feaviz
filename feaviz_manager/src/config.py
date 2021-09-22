from pydantic import BaseSettings


class Settings(BaseSettings):
    http_server_url: str = "http://localhost:9753/object_data"
    keyspace = "demo"

    model_label_path: str = "/Users/lavanyamk/Documents/FeaViz/coco-yolo-v3/coco.names"
    model_weights_path: str = "/Users/lavanyamk/Documents/FeaViz/coco-yolo-v3/yolov3.weights"
    model_cfg_path: str = "/Users/lavanyamk/Documents/FeaViz/coco-yolo-v3/yolov3.cfg"

    superset_base_url: str = "http://localhost:8088/api/v1"

    class Config:
        env_file = ".env"


settings = Settings()
