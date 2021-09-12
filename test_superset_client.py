import openapi_client
from openapi_client import ApiException
from openapi_client.api import security_api
from openapi_client.api.database_api import DatabaseApi
from openapi_client.api.datasets_api import DatasetsApi
from openapi_client.api.dashboards_api import DashboardsApi
from openapi_client.model.dashboard_rest_api_post import DashboardRestApiPost
from openapi_client.model.dataset_rest_api_post import DatasetRestApiPost
from openapi_client.model.inline_object5 import InlineObject5

import json

astradb_schema = "nosql1"
table_name = "image_features_table"
dashboard_name = "openapi_dashboard"
base_url = "http://localhost:8088/api/v1"
def create_chart_table(dashboard_id, datasource_id, chart_name, viz_type, columns):
    query_context={
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
    data_params={"query_mode":"raw", "all_columns": columns}
#     print(json.dumps(data_params))
    data={
    "dashboards": [
      dashboard_id
    ],
    "datasource_id": datasource_id,
    "datasource_type": "table",
    "params":  json.dumps(data_params),
    "query_context": json.dumps(query_context),
    "slice_name": chart_name,
    "viz_type": viz_type
  }
    return requests.post(url= base_url + '/chart/',headers=headers, json=data).json()


def create_dashboard(name):
    return requests.post(url= base_url + '/dashboard/',headers=headers, json={"dashboard_title": name, "published": "true"}).json()

configuration = openapi_client.Configuration(
    host="http://localhost:8088/api/v1",
    username="admin",
    password="admin")
api_client = openapi_client.ApiClient(configuration)

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = security_api.SecurityApi(api_client)
    inline_object5 = InlineObject5(
        password="admin",
        provider="db",
        refresh=True,
        username="admin",
    )  # InlineObject5 |

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.security_login_post(inline_object5)
    except openapi_client.ApiException as e:
        print("Exception when calling SecurityApi->security_login_post: %s\\n" % e)

    api_client.configuration.access_token = str(api_response["access_token"])
    database_api = DatabaseApi(api_client)
    # databases = database_api.database_get()
    # print(databases)

    # api_client.configuration.host="http://localhost:8000/api/v1"
    dataset_api = DatasetsApi(api_client)
    # datasets = dataset_api.dataset_get()
    # print(datasets)

    dataset_id = None
    body = DatasetRestApiPost(database=2, schema=astradb_schema, table_name=table_name)
    try:
        datasets_created = dataset_api.dataset_post(body)
        print(datasets_created)
    except ApiException as e:
        if e.status == 422 and "already exists" in e.body:
            print(str(e.body) + "Fetching dataset ID now...")
            existing_datasets = dataset_api.dataset_get()
            for existing_dataset in existing_datasets["result"]:
                if existing_dataset["schema"] == astradb_schema and existing_dataset["table_name"] == table_name:
                    dataset_id = existing_dataset["id"]
        else:
            raise e

    if dataset_id is None:
        raise Exception("Dataset id is None")
    else:
        print(dataset_id)

    dashboard_api = DashboardsApi(api_client)
    body = DashboardRestApiPost(dashboard_title=dashboard_name, published=True)
    # dashboards = dashboard_api.dashboard_post(body)
    # print(dashboards)

from superset import DatabaseOperation

client = DatabaseOperation("http://localhost:8088", "admin", "admin")
payload = {"dashboard_title": "test", "published": "true"}
response = client.session.post(url=base_url + "/dashboard", json=payload)
print(response.json())
