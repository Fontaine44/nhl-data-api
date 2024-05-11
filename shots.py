from scipy.stats import gaussian_kde
import oracledb
import numpy as np
import pandas as pd
import os

KEY = os.getenv("ORACLE_PASSWORD")

def fetch_shots(params_dict: dict):
    query = """SELECT 
        xCordAdjusted,
        yCordAdjusted,
        period,
        playerPositionThatDidEvent,
        shooterName,
        shooterPlayerId,
        teamCode,
        shotType,
        event,
        strength
        FROM NHL_API.Shots"""

    query_params = []
    parameters = []

    if not all(v is None for v in list(params_dict.values())):         # if there is a parameter
        for key, value in params_dict.items():
            if value:
                parameters.append(value)

                query_params.append(f"{key}=:{key}")

        query += " WHERE " + " AND ".join(query_params)
        query += " AND event != 'MISS'"
    else:
        query += " WHERE event != 'MISS'"

    cs='''(description= (retry_count=10)(retry_delay=1)(address=(protocol=tcps)(port=1522)(host=adb.ca-montreal-1.oraclecloud.com))(connect_data=(service_name=g8776c1047b3446_t37f4p9a1idzstyd_low.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'''

    with oracledb.connect(
        user="NHL_API",
        password=KEY,
        dsn=cs) as conn:

        with conn.cursor() as cursor:
            results = cursor.execute(query, parameters)

            shots = [
                {
                    "xCordAdjusted": shot[0],
                    "yCordAdjusted": shot[1],
                    "period": shot[2],
                    "playerPositionThatDidEvent": shot[3],
                    "shooterName": shot[4],
                    "shooterPlayerId": shot[5],
                    "teamCode": shot[6],
                    "shotType": shot[7],
                    "event": shot[8],
                    "strength": shot[9]
                }
                for shot in results]

    return shots


def kde(shots: list):
    if len(shots) <= 2:
        return []
    df = pd.DataFrame(shots)
    df['yCordAdjusted'] *= -1
    x, y = np.mgrid[0:101, -43:43]
    positions = np.vstack([x.ravel(), y.ravel()])
    values = np.vstack([df['xCordAdjusted'], df['yCordAdjusted']])
    kernel = gaussian_kde(values, bw_method="scott")
    z = np.rot90(np.reshape(kernel(positions).T, (101, 86)))
    return z.tolist()
