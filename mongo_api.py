from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from market_simulator import Market, Point

class ServerUnavailableException(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)

class MongoInterface:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = MongoClient(host, port)
        try:
            self.client.admin.command("ping")
        except ServerSelectionTimeoutError:
            raise ServerUnavailableException(f"MongoDB instance unavailable at {self.host}:{self.port}")
        self.db = self.client.simulations
        self.markets_collection = self.db.markets_collection

    def __find(self, symbol: str, _id=None):
        if _id is not None:
            hits = [i for i in self.markets_collection.find() if i["market_symbol"] == symbol and i["_id"] == _id]
            assert len(hits) == 1
        else:
            hits = [i for i in self.markets_collection.find() if i["market_symbol"] == symbol]
        return hits

    def addMarket(self, market: Market):
        self.markets_collection.insert_one(market.convertToDict())

    def getMarketById(self, _id: str, convert=True):
        market = None
        for i in self.markets_collection.find():
            if _id == i["_id"]:
                if convert:
                    market = Market.convertToMarket(i)
                else:
                    market = i
                break
        return market

    def getMarketBySymbol(self, symbol: str, convert=True):
        markets_raw = self.__find(symbol)
        if convert:
            markets = [Market.convertToMarket(i) for i in markets_raw]
        else:
            markets = markets_raw
        return markets

    def updateMarket(self, _id: str, new_market: Market):
        query = {"_id": _id}
        m = new_market.convertToDict()
        del m["_id"]
        new = {"$set": m}
        self.markets_collection.update_one(query, new)

    def deleteMarket(self, _id: str):
        query = self.getMarketById(_id).convertToDict()
        self.markets_collection.delete_one(query)



