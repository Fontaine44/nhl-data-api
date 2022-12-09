from azure.cosmos import CosmosClient, PartitionKey, ContainerProxy, DatabaseProxy
import json
import os

ENDPOINT = "https://nhl-data.documents.azure.com:443/"
KEY = os.getenv("COSMOS_PK")


def fetch_shots(params_dict: dict):
    query = """SELECT 
        c.playerId,
        c.playerName,
        c.eventTypeId,
        c.secondaryType,
        c["time"],
        c.period,
        c.x,
        c.y,
        c.teamId,
        c.team,
        c.gameId,
        c.strength,
        c.distance
        FROM c"""

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
    
    container = get_cosmos_container("mtl-shots")
    items = container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True)
    return list(items)

    
def get_cosmos_container(name):
    client = CosmosClient(url=ENDPOINT, credential=KEY)
    database = client.get_database_client("nhl-data")
    return database.get_container_client(name)


def drop_data(database: DatabaseProxy):
    try:
        database.delete_container("mtl-shots")
    finally:
        database.create_container("mtl-shots", partition_key=PartitionKey(path='/id'))
        container = database.get_container_client("mtl-shots")

        with open("shots.json", "r") as f:
            data = json.load(f)
        
        for entry in data:
            container.create_item(entry, enable_automatic_id_generation=True)
