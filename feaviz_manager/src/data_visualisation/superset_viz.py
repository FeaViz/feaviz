import requests
import json

from src.config import Settings


def create_chart_table(dashboard_id, datasource_id, chart_name, viz_type, columns):
    query_context = {
        "datasource": {
            "id": datasource_id,
            "type": "table"
        },
        "force": "false",
        "queries": [
            {
                "time_range": "No filter",
                "filters": [],
                "extras": {
                    "time_grain_sqla": "P1D",
                    "time_range_endpoints": [
                        "inclusive",
                        "exclusive"
                    ],
                    "having": "",
                    "having_druid": [],
                    "where": ""
                },
                "applied_time_extras": {},
                "columns": columns,
                "orderby": [],
                "annotation_layers": [],
                "row_limit": 10000,
                "timeseries_limit": 0,
                "order_desc": "true",
                "url_params": {},
                "custom_params": {},
                "custom_form_data": {},
                "post_processing": []
            }
        ],
        "result_format": "json",
        "result_type": "full"
    }
    data_params = {"query_mode": "raw", "all_columns": columns}
    data = {
        "dashboards": [
            dashboard_id
        ],
        "datasource_id": datasource_id,
        "datasource_type": "table",
        "params": json.dumps(data_params),
        "query_context": json.dumps(query_context),
        "slice_name": chart_name,
        "viz_type": viz_type
    }
    return requests.post(url=Settings.superset_base_url + '/chart/', headers=Settings.headers, json=data).json()


def create_chart_histogram(dashboard_id, datasource_id, chart_name, viz_type, columns):
    query_context = {
        "datasource": {
            "id": datasource_id,
            "type": "table"
        },
        "force": "false",
        "queries": [
            {
                "time_range": "No filter",
                "filters": [],
                "extras": {
                    "time_grain_sqla": "P1D",
                    "time_range_endpoints": [
                        "inclusive",
                        "exclusive"
                    ],
                    "having": "",
                    "having_druid": [],
                    "where": ""
                },
                "applied_time_extras": {},
                "columns": [],
                "orderby": [],
                "annotation_layers": [],
                "row_limit": 10000,
                "timeseries_limit": 0,
                "order_desc": "true",
                "url_params": {},
                "custom_params": {},
                "custom_form_data": {},
                "post_processing": []
            }
        ],
        "result_format": "json",
        "result_type": "full"
    }
    data_params = json.dumps({"all_columns_x": columns, "viz_type": viz_type})
    data = {
        "dashboards": [
            dashboard_id
        ],
        "datasource_id": datasource_id,
        "datasource_type": "table",
        "params": json.dumps(data_params),
        "query_context": json.dumps(query_context),
        "slice_name": chart_name,
        "viz_type": viz_type
    }
    return requests.post(url=Settings.superset_base_url + '/chart/', headers=Settings.headers, json=data).json()
