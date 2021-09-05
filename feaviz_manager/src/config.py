from pydantic import BaseSettings


class Settings(BaseSettings):
    http_server_url: str = "http://localhost:9753/object_data"
    keyspace = "demo"

    model_label_path: str = "/Users/lavanyamk/Documents/FeaViz/coco-yolo-v3/coco.names"
    model_weights_path: str = "/Users/lavanyamk/Documents/FeaViz/coco-yolo-v3/yolov3.weights"
    model_cfg_path: str = "/Users/lavanyamk/Documents/FeaViz/coco-yolo-v3/yolov3.cfg"

    superset_base_url = "http://localhost:8088/api/v1"
    astradb_schema = "nosql1"
    # Unable to authenticate using JWT token. Raise issue with Superset
    cookie = '_xsrf=2|a3adf84d|5c49d8543aa089ba66e81b78ae331837|1609085664; csrftoken=hEr9DwOP6Q1OGs5IumLRsf1bZKnyQpkafc36OW1rF57yaCnLe80dP8CbqnFqPU7H; username-localhost-8888="2|1:0|10:1628864973|23:username-localhost-8888|44:NWIzYWY2NTQ0NGI1NGRjYmIyYTkyMzcxNWNmOTliZWI=|bd4090b101354da9c0e428ea15f1679efcf32457de2c8eb40f1572f19e45cf9a"; username-localhost-8889="2|1:0|10:1630251336|23:username-localhost-8889|44:ODVhMWFkZjI0NmFjNDk5NjkyYTc3MTFjNzA5Y2M4OTQ=|a1ffb9c1c9310814d08ebc39e10646c204d50c322552e6bda41df2c7f4960c1b"; session=.eJytkc1KxTAQhd8l60In_5O-ikiZJBNbLDeS5C5EfHfjdSu4cTOr853zwXyIvTTuh9hGu_Mi9jOLTVC2EGNE7dAQGJIhgirJlJwgA0VDKI22BKycLQiYMDhjnMUQgMhLlbWxGJloMtaAitGhS4CuSLA6M7lIkK02s8yy86qohJIKKFUyikWk3so-6ivfpo_0wXo9pTCkoKQ3gFGh8chz0jpNkmQuiSd31UQXT2aCi3ijF96Ps4_a3sX2JI4x3rZ1fYSO2sc23XG9d279cc9bqevkfs-1enFfr1n3V4bzOVb1f0XPi_jW-_mOFJ9foreG0Q.YTOiZg.MVW-FIwg2m03u0srAZwMPKruJtw'
    headers = {'user-accept': 'application/json', 'Content-Type': 'application/json', '': cookie}


settings = Settings()
