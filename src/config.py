import yaml

base_config = {
  'ITEMS_URL': 'https://api.hypixel.net/resources/skyblock/items',
  'AUCTIONS_ENDED':'https://api.hypixel.net/skyblock/auctions_ended',
  'AUCTIONS_CURRENT': 'https://api.hypixel.net/skyblock/auctions',
  'AUCTION_LOOKUP': 'https://api.hypixel.net/skyblock/auction',
  'AUCTION_LOOKUP': 'https://api.hypixel.net/skyblock/auction',
  'API_KEY': 'bad',
}


def initConfig():
  try:

    with open("config.yml", "r") as f:
      print("Config found")

  except FileNotFoundError as e:
    print("No config found, creating now...")

    with open("config.yml", "w") as f:

      data = yaml.dump(base_config, f)
      print("Write successful")


def getItemsUrl() -> str:
  with open("config.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

    return data['ITEMS_URL']

def getAuctionsEndedUrl() -> str:
  with open("config.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    return data['AUCTIONS_ENDED']


def getAuctionsUrl() -> str:
  with open("config.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    return data['AUCTIONS_CURRENT']

def getAuctionLookupUrl() -> str:
  with open("config.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    return data['AUCTION_LOOKUP']


def getAPIKey() -> str:
  with open("config.yml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    return data['API_KEY']