import pathlib
import threading
import requests

from mysql.connector import connection
from auctions import auction_close_loop, run_auctions
from config import initConfig

from items import checkItems

BASE_URL = 'https://api.hypixel.net/skyblock'


def getRecentlyEndedAuctions():
    r = requests.get(BASE_URL + '/auctions_ended')

    js = r.json()
    pathlib.Path('data.json').write_bytes(r.content)


def main():
    initConfig()
    checkItems()

    th1 = threading.Thread(target=run_auctions)
    th2 = threading.Thread(target=auction_close_loop)
    print("Starting mass collection of auctions")
    th1.start()
    th2.start()

    th1.join()
    print("Mass collection stopped")

    th2.join()
    print("Done")


if __name__ == "__main__":
    main()
