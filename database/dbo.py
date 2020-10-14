import sys
import logging
import traceback
import unidecode

from database.connect import get_connect


def check_padron(razon_social):

    row = None
    connection = None

    try:
        connection = get_connect()
        cursor = connection.cursor()

        sql_statement = "SELECT cuit, razon from padron "
        sql_statement += " where LOWER(razon_spaces) LIKE %s"
        sql_statement += "    or LOWER(razon_spaces) LIKE %s"

        razon_social_u = unidecode.unidecode(razon_social)

        args = ['%' + razon_social[0:25] + '%',
                '%' + razon_social_u[0:25] + '%']

        cursor.execute(sql_statement, args)
        row = cursor.fetchone()

        cursor.close()

    except (Exception) as error:
        logging.error('Error at %s', exc_info=error)

    finally:
        if(connection):
            connection.close()

    return row


def insert_parsed(cuit, razon, money, url):

    try:
        connection = get_connect()
        cursor = connection.cursor()

        statement = """ INSERT INTO boletin_parsed (cuit, razon, money, url) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (cuit, razon, money, url)
        cursor.execute(statement, record_to_insert)

        connection.commit()
        count = cursor.rowcount

    except (Exception) as error:
        logging.error('Error at %s', exc_info=error)

    finally:
        if(connection):
            cursor.close()
            connection.close()
