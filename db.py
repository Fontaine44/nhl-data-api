from azure.cosmos import CosmosClient
import datetime
import os

ENDPOINT = "https://nhl-data.documents.azure.com:443/"
KEY = os.getenv("COSMOS_PK")
DATABASE_NAME = "nhl-data"
CONTAINER_NAME = "export-log"


def fetch_logs(params_dict: dict):

    if params_dict["date"] is None:
        params_dict["date"] = str(datetime.date.today())

    query = """SELECT c.log FROM c"""

    query_params = []
    parameters = []

    if not all(v is None for v in list(params_dict.values())):         # if there is a parameter
        for key, value in params_dict.items():
            if value:
                parameters.append({
                    "name": "@"+key,
                    "value": value
                })

                query_params.append(f"c.{key}=@{key}")

        query += " WHERE " + " AND ".join(query_params)

    with CosmosClient(url=ENDPOINT, credential=KEY) as client:
        client = CosmosClient(url=ENDPOINT, credential=KEY)
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)
        results = container.query_items(
            query=query, parameters=parameters, enable_cross_partition_query=True)
        logs = [log for log in results]

    if not logs:
        return "No logs available"
    else:
        logs_string = ""
        for log in logs:
            logs_string += log["log"] + "\n"
        return logs_string
