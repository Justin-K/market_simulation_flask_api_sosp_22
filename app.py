from flask import Flask, jsonify, request
from mongo_api import MongoInterface
from market_simulator import MarketSimulator, Market, Point

app = Flask(__name__)
mi = MongoInterface("127.0.0.1", 27017)
ms = MarketSimulator(500, 0, 100)

@app.route("/")
def index():
    return "<h1>Market Simulation API</h1>" \
           "<p>This API was created for Summer of Side Projects 2022 by Justin (anon_104)." \
           "It was created as a simple proof-of-concept and for educational purposes. It is not useful in any meaningful " \
           "way unfortunately, but it helped me learn what Flask is and what HTTP requests are.</p>"


@app.route("/fetch/all", methods=["GET"])
def get_all_sims():
    return jsonify([i for i in mi.markets_collection.find()])


@app.route("/generate/<string:symbol>", methods=["GET"])
def generate_and_store(symbol: str):
    mi.addMarket(ms.simulate(symbol))
    return {"success": "true"}


@app.route("/fetch/id/<string:_id>", methods=["GET"])
def get_by_id(_id):
    return mi.getMarketById(_id, convert=False)


@app.route("/fetch/symbol/<string:symbol>", methods=["GET"])
def get_by_symbol(symbol):
    return jsonify(mi.getMarketBySymbol(symbol, convert=False))


@app.route("/update/id/<string:_id>", methods=["PUT"])
def update_market(_id):
    payload = request.get_json()
    m = Market(payload["symbol"].upper())
    for i in payload["points"]:
        m.addPoint(Point.convertToPoint(i))
    mi.updateMarket(_id, m)
    return {"success": "true"}


@app.route("/delete/id/<string:_id>", methods=["DELETE"])
def delete_market(_id):
    mi.deleteMarket(_id)
    return {"success": "true"}


@app.route("/add", methods=["POST"])
def add_market():
    payload = request.get_json()
    m = Market(payload["symbol"].upper())
    for i in payload["points"]:
        m.addPoint(Point.convertToPoint(i))
    mi.addMarket(m)
    return {"success" : "true"}
