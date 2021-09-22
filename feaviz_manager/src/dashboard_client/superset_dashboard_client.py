import json


class SupersetDashboardClient:

    def __init__(self, superset_session_client, superset_openapi_client):
        self.superset_session_client = superset_session_client
        self.superset_openapi_client = superset_openapi_client

    def create_chart_table(self, dashboard_id, datasource_id, chart_name, viz_type, columns):
        query_context = {
            "datasource": {
                "id": datasource_id,
                "type": "table"
            }
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
        return self.superset_session_client.session.post(url=base_url + '/chart/', json=data).json()

    def create_chart_histogram(self, dashboard_id, datasource_id, chart_name, viz_type, columns):
        query_context = {
            "datasource": {
                "id": datasource_id,
                "type": "table"
            }
        }
        data_params = {
            "all_columns_x": columns,
            "viz_type": viz_type
        }
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
        return self.superset_session_client.session.post(url=base_url + '/chart/', json=data).json()

    def create_chart_bar(self, dashboard_id, datasource_id, chart_name, viz_type, columns, group_by_columns):
        query_context = {
            "datasource": {
                "id": datasource_id,
                "type": "table"
            },
            "queries": [{
                "columns": [
                    columns
                ],
                "metrics": [
                    "count"
                ]
            }
            ]
        }
        data_params = {
            "groupby": group_by_columns,
            "viz_type": viz_type,
            "metrics": ["count"],
            "order_desc": True
        }

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
        return self.superset_session_client.session.post(url=base_url + '/chart/', json=data).json()

    def create_structured_data_viz(self):
        return "0"