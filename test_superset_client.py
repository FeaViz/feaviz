import openapi_client
from openapi_client.api import security_api
from openapi_client.api.database_api import DatabaseApi
from openapi_client.api.datasets_api import DatasetsApi
from openapi_client.model.inline_object5 import InlineObject5
from pprint import pprint

configuration = openapi_client.Configuration(
    host= "http://localhost:8088/api/v1",
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
    ) # InlineObject5 |

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.security_login_post(inline_object5)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling SecurityApi->security_login_post: %s\\n" % e)

    api_client.configuration.access_token = str(api_response["access_token"])
    database_api = DatabaseApi(api_client)
    databases = database_api.database_get()
    print(databases)

    # api_client.configuration.host="http://localhost:8000/api/v1"
    dataset_api = DatasetsApi(api_client)
    dataset_api.dataset_get()



