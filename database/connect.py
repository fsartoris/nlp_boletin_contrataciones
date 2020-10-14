import os
import pymysql
from configparser import ConfigParser

def config():
    db = {}
    db['database'] = os.environ.get('DB_DATABASE', None)
    db['user'] = os.environ.get('DB_USER', None)
    db['password'] = os.environ.get('DB_PASSWORD', None)
    db['host'] = os.environ.get('DB_HOST', None)
    #db['auth_plugin'] =  os.environ.get('DB_AUTH', None)
    return db


def get_connect():
    try:
        params = config()
        connection = pymysql.connect(**params)

    except (Exception) as error:
        if(connection):
            print("Failed to connect db", error)

    finally:
        return connection
