import oracledb
import datetime
import os

ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
CONNECTION_STR = "(description= (retry_count=2)(retry_delay=2)(address=(protocol=tcps)(port=1521)(host=adb.ca-montreal-1.oraclecloud.com))(connect_data=(service_name=g8776c1047b3446_fkmjnxbscms692ba_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))"

def fetch_logs(date):

    if date is None:
        date = str(datetime.date.today())

    query = "SELECT LOG FROM NHL_API.EXPORT_LOGS WHERE TRUNC(EXPORT_DATE) = TO_DATE(:1, 'YYYY-MM-DD')"

    with oracledb.connect(
        user="NHL_API",
        password=ORACLE_PASSWORD,
        dsn=CONNECTION_STR) as conn:

        cursor = conn.cursor()
        cursor.execute(query, (date,))
    
        logs = cursor.fetchall()

        if not logs:
            return "No logs available"
        else:
            logs_string = ""
            for log in logs:
                logs_string += log[0] + "\n"
            return logs_string
