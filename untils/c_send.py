import json
import requests
import pymysql

from config.config import DB_PORT, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

REGISTER_FIELD_MAP = {
    "mobile": "mobile",
    "email": "email",
}

def send_http(data,session = None):
    if session is None:
        session = requests.Session()
    return session.request(**data)


def send_sql(sql,params = None ,index = 0):

    conn = pymysql.connect(
        host=DB_HOST,
        port = DB_PORT,
        database=DB_NAME,
        user = DB_USER,
        password=DB_PASSWORD
    )
    curs = conn.cursor()
    curs.execute(sql, params)
    result = curs.fetchone()
    curs.close()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return None
def execute_sql(sql,params = None):
    conn = pymysql.connect(
        host=DB_HOST,
        port = DB_PORT,
        database=DB_NAME,
        user = DB_USER,
        password=DB_PASSWORD
    )
    curs = conn.cursor()
    curs.execute(sql, params)
    conn.commit()
    curs.close()
    conn.close()



def find_sql(case):
    registerType = case['json']['registerType']
    user = case['json']['account']
    if registerType in REGISTER_FIELD_MAP:
        sql=f"SELECT {registerType} FROM users WHERE {registerType} = %s"
        return send_sql(sql, (user,))
def delete_sql(case):
    registerType = case['json']['registerType']
    user = case['json']['account']
    if registerType in REGISTER_FIELD_MAP:
        sql=f"DELETE FROM users WHERE {registerType} = %s"
        return execute_sql(sql, (user,))

