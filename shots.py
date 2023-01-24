from azure.cosmos import CosmosClient
from scipy.stats import gaussian_kde
import numpy as np
import pandas as pd
import os

ENDPOINT = "https://nhl-data.documents.azure.com:443/"
KEY = os.getenv("COSMOS_PK")
DATABASE_NAME = "nhl-data"
CONTAINER_NAME = "nhl-shots"


def fetch_shots(params_dict: dict):
    query = """SELECT 
        c.xCordAdjusted,
        c.yCordAdjusted,
        c.period,
        c.playerPositionThatDidEvent,
        c.shooterName,
        c.shooterPlayerId,
        c.teamCode,
        c.shotType,
        c.event,
        c.strength
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
        query += ' AND c.event != "MISS"'
    else:
        query += ' WHERE c.event != "MISS"'

    with CosmosClient(url=ENDPOINT, credential=KEY) as client:
        client = CosmosClient(url=ENDPOINT, credential=KEY)
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)
        results = container.query_items(
            query=query, parameters=parameters, enable_cross_partition_query=True)
        shots = [shot for shot in results]

    return shots


def kde(shots: list):
    if len(shots) <= 1:
        return []
    df = pd.DataFrame(shots)
    df['yCordAdjusted'] *= -1
    x, y = np.mgrid[0:101, -43:43]
    positions = np.vstack([x.ravel(), y.ravel()])
    values = np.vstack([df['xCordAdjusted'], df['yCordAdjusted']])
    kernel = gaussian_kde(values, bw_method="scott")
    z = np.rot90(np.reshape(kernel(positions).T, (101, 86)))
    return z.tolist()
