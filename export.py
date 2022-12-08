from azure.cosmos import CosmosClient, PartitionKey, ContainerProxy, DatabaseProxy
import json
import os


def run():
    endpoint = "https://nhl-data.documents.azure.com:443/"
    key = os.getenv("COSMOS_PK")
    
    client = CosmosClient(url=endpoint, credential=key)
    database = client.get_database_client("nhl-data")

    return query_all_shots(database.get_container_client("mtl-shots"))


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


def query_all_shots(container: ContainerProxy):
    qu = """SELECT 
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
            FROM c
            WHERE c.strength=@strength
            AND c.playerName=@playerName
            """

    params = [
        {
            "name":"@strength",
            "value":"PP"
        },
        {
            "name":"@playerName",
            "value":"Cole Caufield"
        }
    ]

    items = container.query_items(query=qu, parameters=params, enable_cross_partition_query=True)
    it = list(items)
    return it

if __name__ == "__main__":
    run()
