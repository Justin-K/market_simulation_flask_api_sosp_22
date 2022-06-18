from __future__ import annotations
from random import uniform, random
import matplotlib.pyplot as plt
from function_lib import randOp, clamp, avg, generateRandomAlphanumericString


class Point:

    def __init__(self, x, y):
        self.x_coordinate = x
        self.y_coordinate = y

    def __repr__(self):
        return f"({self.x_coordinate}, {self.y_coordinate})"

    def __eq__(self, other):
        if self.x_coordinate == other.x_coordinate and self.y_coordinate == other.y_coordinate:
            return True
        else:
            return False

    def convertToList(self):
        return [self.x_coordinate, self.y_coordinate]

    @staticmethod
    def convertToPoint(ls: list):
        return Point(ls[0], ls[1])


class Market:

    def __init__(self, market_symbol: str, points=None):
        if points is None:
            self._points = []
        else:
            self._points = points
        self.symbol = market_symbol.upper()
        self.ID = generateRandomAlphanumericString(15)

    def __repr__(self):
        return f"Symbol: {self.symbol}\n" \
               f"ID: {self.ID}" \
               f"Points: {[i for i in self._points]}"

    def __getitem__(self, item: int) -> Point:
        return self._points[item]

    def addPoint(self, point: Point):
        self._points.append(point)

    def simplify(self, iterations):  # this function is relatively rough
        pnts = self._points.copy()
        for _ in range(iterations):
            new_pnts = []
            for i in range(len(pnts)):
                if i != len(pnts)-1:
                    first = pnts[i]
                    second = pnts[i+1]
                    new_pnts.append(Point(i, avg([first.y_coordinate, second.y_coordinate])))
                else:
                    pnts = new_pnts
                    break
        return Market(self.symbol, points=pnts)

    def graph(self):
        if self._points:
            plt.plot([i.x_coordinate for i in self._points], [i.y_coordinate for i in self._points])
            plt.title(self.symbol)
            plt.show()

    def convertPoints(self):
        return [i.convertToList() for i in self._points]

    def convertToDict(self) -> dict:
        return {"_id": self.ID, "market_symbol": self.symbol, "points": [Point.convertToList(i) for i in self._points]}

    @staticmethod
    def convertToMarket(dict_obj: dict) -> Market:
        pnts = [Point.convertToPoint(i) for i in dict_obj["points"]]
        x = Market(dict_obj["market_symbol"], points=pnts)
        x.ID = dict_obj["_id"]
        return x




class MarketSimulator:

    def __init__(self, num_iterations: int, abs_min, abs_max, relative_scalar=10):
        self.iterations = num_iterations
        self.abs_min = abs_min
        self.abs_max = abs_max
        self.rel_max = self.abs_max/relative_scalar
        self.rel_min = -self.rel_max

    def simulate(self, symbol) -> Market:
        new_market = Market(symbol)
        new_market.addPoint(Point(1, uniform(self.abs_min, self.abs_max)))
        for i in range(1, self.iterations):
            prev_y = abs(new_market[i-1].y_coordinate)
            deviation = uniform(self.rel_min, self.rel_max)
            new_pnt = randOp(prev_y, deviation)
            new_pnt = clamp(new_pnt, self.abs_min, self.abs_max)
            if random() > random():
                new_market.addPoint(Point(i+random(), new_market[i-1].y_coordinate))
            else:
                new_market.addPoint(Point(i, new_pnt))
        return new_market


