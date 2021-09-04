from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from .config import settings


class DataPath(BaseModel):
    path: str


app = FastAPI()


@app.post("/tables/")
def create_course(tabular_data_path: DataPath):
    create_tablular_data_visualization(tabular_data_path)
    return tabular

@app.post("/images")
def read_root(images_data_path: DataPath):
    create_image_data_visualization(images_data_path, settings.http_server_url,
                                    settings.model_label_path, settings.model_weights_path,
                                    settings.model_cfg_path)
    return images