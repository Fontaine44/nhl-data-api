from azure.cosmos import CosmosClient
from scipy.stats import gaussian_kde
import numpy as np
import pandas as pd
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
        c.distance,
        c.crossRed
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


def kde(shots: list):
    df = pd.DataFrame(shots)
    df = df.query("x > 24 and crossRed == True")   # remove shots outside the zone
    df['y'] *= -1
    x, y = np.mgrid[0:101, -43:43]
    positions = np.vstack([x.ravel(), y.ravel()])
    values = np.vstack([df['x'], df['y']])
    kernel = gaussian_kde(values, bw_method="scott")
    z = np.rot90(np.reshape(kernel(positions).T, (101,86)))
    return z.tolist()