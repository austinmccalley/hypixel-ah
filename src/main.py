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

  th = threading.Thread(target=run_auctions)
  print("Starting mass collection of auctions")
  th.start()
  auction_close_loop()

  th.join()
  print("Mass collection stopped")



if __name__ == "__main__":
  main()