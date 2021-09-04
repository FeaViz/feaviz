import openapi_client
from openapi_client.api.dashboards_api import DashboardsApi
configuration = openapi_client.Configuration(
    host= "http://localhost:8088/api/v1",
    username="admin",
    password="admin")
api_client = openapi_client.ApiClient(configuration)
dashboard_api = DashboardsApi(api_client)
dashboards = dashboard_api.dashboard_get()
print(dashboards)