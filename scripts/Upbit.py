import jwt
import uuid
import json
import requests

from pprint import pprint

URL = {
    "ASSET_URL": "https://api.upbit.com/v1/accounts",
    "MARKET_URL": "https://api.upbit.com/v1/candles/days"
}

class Upbit:
    def __init__(self, keys):
        self.ACCESS_KEY = keys["ACCESS_KEY"]
        self.SECRET_KEY = keys["SECRET_KEY"]
        self.ASSET = {}
        self.STOCKED_SYMBOL = []
        self.KRW = 0
        self.MARGIN = 0

    def get_asset(self, file: bool):
        if self.ASSET:
            self.ASSET = {}
            self.STOCKED_SYMBOL = []
            self.KRW = 0
            self.MARGIN = 0

        payload = {
            "access_key": self.ACCESS_KEY,
            "nonce": str(uuid.uuid4())
        }

        jwt_token = jwt.encode(payload, self.SECRET_KEY)
        authorization_token = f"Bearer {jwt_token}"

        headers = {
            "Authorization": authorization_token
        }

        asj = requests.get(URL["ASSET_URL"], headers=headers).json()

        for raw in asj:
            bid = raw["avg_buy_price"]
            currency = raw["currency"]
            balance = raw["balance"]
            unit_currency = raw["unit_currency"]

            if not bid == "0":
                self.ASSET[currency] = {
                    "stocked": True,
                    "market": unit_currency,
                    "balance": float(balance),
                    "bid": float(bid)
                }
            else:
                if currency == "KRW":
                    self.KRW = int(float(balance))
                else: 
                    self.ASSET[currency] = {
                        "stocked": False,
                        "balance": float(balance)
                    }

        self.get_market_price()
        # self.wallet(file)

    def get_market_price(self):
        for symbol in self.ASSET.keys():
            flag = self.ASSET[symbol]["stocked"]

            if flag and symbol != "portfolio":
                self.STOCKED_SYMBOL.append(symbol)

        headers = {
            "Accept": "application/json"
        }

        querystring = {
            "market": "",
            "count": "0"
        }

        if not len(self.STOCKED_SYMBOL):
            self.ASSET["None"] = "STOCKED COIN DOES NOT EXIST"
        else:
            for symbol in self.STOCKED_SYMBOL:
                if self.ASSET[symbol]["stocked"]:
                    # TODO: SEPERATE MARKET(KRW, BTC, USDT)
                    querystring["market"] = f"BTC-MASK"

                    response = requests.request("GET", URL["MARKET_URL"], headers=headers, params=querystring).json()

                    pprint(response, indent=4)

                    # TODO: NEED TRANSACTION OF BTC PRICE, response[0]["trade_price"]
                    # self.ASSET[symbol]["quote"] = float(response[0]["trade_price"])

    def wallet(self, file=False):
        
        # stocked: 상장 현황
        # market: 마켓(KRW, BTC, USDT, BUSD, ETH, .``..)
        # balance: 보유 수량
        # bid: 매수 평균가
        # quote: 현재가
        # blended_price: 매수금액
        # market_price: 평가금액
        # return: 손익금액
        # margin: 평가손익
        # weight: 비중

        if "None" in self.ASSET.keys():
            self.ASSET["portfolio"] = {
                "total_asset": self.KRW,
                "KRW": self.KRW,
                "total_blended_price": "N/A",
                "total_market_price": "N/A",
                "total_return": "N/A",
                "margin_average": "N/A"
            }
        else:
            try:
                total_blended_price = 0
                total_market_price = 0

                for ticker in self.STOCKED_SYMBOL:
                    coin = self.ASSET[ticker]

                    balance = coin["balance"]
                    bid = coin["bid"]
                    quote = coin["quote"]

                    blended_price = balance * bid
                    market_price = balance * quote
                    return_price = market_price - blended_price

                    coin["quote"] = quote
                    coin["blended_price"] = blended_price
                    coin["market_price"] = market_price
                    coin["return"] = round(return_price, 2)
                    coin["margin"] = "{:.2f}%".format(percentage(return_price, blended_price))

                    total_blended_price += blended_price
                    total_market_price += market_price

                total_return = total_market_price - total_blended_price
                margin_average = percentage(total_return, total_blended_price)
                total_asset = int(self.KRW + total_market_price)

                self.MARGIN = round(margin_average, 2)

                for ticker in self.STOCKED_SYMBOL:
                    coin = self.ASSET[ticker]

                    coin["weight"] = "{:.1f}%".format(percentage(coin["market_price"], total_asset))

                self.ASSET["portfolio"] = {
                    "total_asset": total_asset,
                    "KRW": self.KRW,
                    "KRW_weight": f"{round(percentage(self.KRW, total_asset), 2)}%",
                    "total_blended_price": int(total_blended_price),
                    "total_market_price": int(total_market_price),
                    "total_return": int(total_return),
                    "margin_average": "{:.2f}%".format(margin_average)
                }
            except ZeroDivisionError:
                pass
        
        if (file):
            with open("./caches/asset.json", "w") as handle:
                json.dump(self.ASSET, handle, indent=4)

def percentage(numerator, denominator):
    return numerator / denominator * 100