from mysql.connector import (connection, errorcode)
import mysql.connector
import requests
from tqdm import tqdm

from config import getItemsUrl


def checkItems():
    try:
        cnx = connection.MySQLConnection(
            user="austin", password="password", database="hypixel_ah", port=6033)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:

        cursor = cnx.cursor()

        print("Checking items db...")

        query = "SELECT COUNT(*) from `items`"
        cursor.execute(query)  # execute query separately
        res = cursor.fetchone()
        total_rows = res[0]  # total rows
        cursor.close()

        print("Found %s rows" % total_rows)

        if total_rows == 0:
            populateItems(cnx)

        cnx.close()


def populateItems(cnx: connection.MySQLConnection):
    ITEMS_URL = getItemsUrl()

    r = requests.get(ITEMS_URL)

    rjson = r.json()

    itemsFound = rjson['items']

    add_item = (
        "INSERT INTO `items` (id, name, tier, material) VALUES(%s, %s, %s, %s)")

    for itm in tqdm(itemsFound):
        if 'tier' in itm:
            tier = itm['tier']
        else:
            tier = 'UNKNOWN'

        data_item = (itm['id'], itm['name'], tier, itm['material'])

        cursor = cnx.cursor()
        cursor.execute(add_item, data_item)

        cnx.commit()

        cursor.close()
