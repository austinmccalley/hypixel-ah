import json
import time
import pycron
import requests
from tqdm import tqdm
from mysql.connector import (connection, errorcode)
import mysql.connector

from config import getAPIKey, getAuctionLookupUrl, getAuctionsEndedUrl, getAuctionsUrl
from util import decode_nbt, parse_color, unpack_nbt


def get_closed_auctions():
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

        AUCTION_URL = getAuctionsEndedUrl()

        r = requests.get(AUCTION_URL)

        rjson = r.json()

        print(len(rjson['auctions']))

        update_auction = (
            "UPDATE `auctions` SET `price`='%s',`closed`='%s' WHERE `id`=%s")

        for itm in (rjson['auctions']):

            item_bytes = itm['item_bytes']

            nbt_obj = decode_nbt(item_bytes)
            item = unpack_nbt(nbt_obj)

            if 'i' not in item or len(item['i']) < 1:
                print("ERROR\n")
                print(itm)
                continue

            item = item['i'][0]

            price = itm['price']
            auction_id = itm['auction_id']
            data_auction = (price, 1, auction_id)

            cursor = cnx.cursor()
            cursor.execute(update_auction, data_auction)
            cnx.commit()
            cursor.close()

        cnx.close()


def get_auction(auction_id):
    # 40ec1af8-057e-44e2-8b05-2dd6dd3597a8
    API_KEY = getAPIKey()
    AUCTION_LOOKUP = getAuctionLookupUrl()


def run_auctions():
    while True:
        if pycron.is_now('0 * * * *'):  # Every hour
            get_open_auctions(0)

            time.sleep(60)


def get_open_auctions(curr=0):
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
        AUCTION_URL = getAuctionsUrl()

        built_url = AUCTION_URL + '?page=' + str(curr)

        r = requests.get(built_url)

        rjson = r.json()

        if 'page' not in rjson or rjson['page'] == rjson['totalPages']:
            return

        add_auction = (
            "INSERT IGNORE INTO `auctions`(`id`, `item`, `name`, `price`, `bin`, `closed`, `lore`, `start`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")

        for itm in rjson['auctions']:

            item_bytes = itm['item_bytes']

            nbt_obj = decode_nbt(item_bytes)
            item = unpack_nbt(nbt_obj)

            if 'i' not in item or len(item['i']) < 1:
                print("ERROR\n")
                print(itm)
                continue

            item = item['i'][0]

            item_id = item['tag']['ExtraAttributes']['id']
            name = item['tag']['display']['Name']
            price = itm['starting_bid']
            bin = bool(itm['bin'])
            auction_id = itm['uuid']
            lore = parse_color(itm['item_lore'], True)

            data_auction = (auction_id, item_id, name, 0, bin, 0, lore, price)

            cursor = cnx.cursor()
            cursor.execute(add_auction, data_auction)
            cnx.commit()
            cursor.close()

        cnx.close()
        new_curr = curr + 1
        get_open_auctions(new_curr)


def auction_close_loop():
    while True:
        if pycron.is_now('* * * * *'):  # Every minute
            get_closed_auctions()

            time.sleep(60)
