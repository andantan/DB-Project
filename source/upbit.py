import jwt
import uuid
import requests
import math


URL = {
    "ASSET_URL": "https://api.upbit.com/v1/accounts",
    "MARKET_URL": "https://api.upbit.com/v1/candles/days"
}

UPBIT_STOCKED_TICKER_SYMBOL = [
    "BTC", "ETH", "BCH", "AAVE", "BSV", "SOL", "STRK",
    "AVAX", "BTG", "ETC", "AXS", "NEO", "REP", "DOT",
    "ATOM", "LINK", "WAVES", "NEAR", "SBD", "WEMIX", "QTUM",
    "GAS", "OMG", "TON", "KAVA", "FLOW", "MTL", "XTZ", "KNC",
    "AQT", "THETA", "LSK", "CBK", "SAND", "EOS", "CELO", "SRM",
    "MANA", "DAWN", "GMT", "1INCH", "STORJ", "ADA", "ENJ", "STRAX",
    "ARK", "PUNDIX", "MATIC", "SXP", "HUNT", "BAT", "HIVE", "STX",
    "MLK", "ONG", "GRS", "PLA", "XRP", "ALGO", "BORA", "IOTA", "ICX",
    "ZRX", "GLM", "ONT", "STEEM", "POWR", "HUM", "NU", "CVC", "ELF",
    "CRO", "XLM", "AERGO", "ADAR", "CHZ", "WAXP", "MOC", "UPP",
    "HBAR", "TRX", "DOGE", "FCT2", "TFUEL", "DKA", "LOOM", "STPT",
    "ORBS", "XEM", "ZIL", "META", "T", "ANKR", "JST", "SNT", "VET",
    "SSX", "MED", "IOST", "QKC", "STMX", "RFR", "AHT", "TT", "MVL",
    "IQ", "CRE", "SC", "MFT", "MBL", "XEC", "BTT"  
]

class Upbit:
    def __init__(self, keys: dict) -> None:
        self.ACCESS_KEY = keys["ACCESS_KEY"]
        self.SECRET_KEY = keys["SECRET_KEY"]
        
        
    def request_asset(self) -> list[dict]: 
        payload = {
            "access_key": self.ACCESS_KEY,
            "nonce": str(uuid.uuid4())
        }
        
        authorization_token = f"Bearer {jwt.encode(payload, self.SECRET_KEY)}"
        
        headers = {
            "Authorization": authorization_token
        }
        
        raw_wallet = requests.get(URL["ASSET_URL"], headers=headers).json()
        
        return raw_wallet
        
        
    def cooking_raw_wallet(self, raw_asset: list[dict]) -> list:
        headers = {
            "Accept": "application/json"
        }
        
        STSL = "STOCKED_TICKER_SYMBOL_LIST"
        STIL = "STOCKED_TICKER_INFO_LIST"
        UTSL = "UNSTOCKED_TICKER_SYMBOL_LIST"
        UTIL = "UNSTOCKED_TICKER_INFO_LIST"
        KRW = "KRW"
        
        asset = dict()
        
        asset[KRW] = int(float(raw_asset[0]["balance"]))
        asset[STSL] = list()
        asset[UTSL] = list()
        asset[STIL] = dict()
        asset[UTIL] = dict()
        
        for ticker in raw_asset[1: ]:
            SYMBOL = ticker["currency"]
            
            if SYMBOL not in UPBIT_STOCKED_TICKER_SYMBOL:
                asset[UTSL].append(SYMBOL)
            
                asset[UTIL][SYMBOL] = {
                    "HOLDING_BALANCE" : float(ticker["balance"])
                }
                
                continue
        
            querystring = {
                "market": f"KRW-{SYMBOL}",
                "count": "0"
            }
            
            MARKET_PRICE = requests.request("GET", URL["MARKET_URL"], headers=headers, params=querystring).json()[0]["trade_price"] # 현재 시장가
            AVERAGE_PRICE = float(ticker["avg_buy_price"]) # 평단가
            HOLDING_BALANCE = float(ticker["balance"]) # 보유 개수
            BID_PRICE = math.floor(AVERAGE_PRICE * HOLDING_BALANCE) # 매수 금액
            EVALUATE_PRICE = math.floor(MARKET_PRICE * HOLDING_BALANCE) # 평가 금액
            EVALUATE_RETURN = EVALUATE_PRICE - BID_PRICE  # 평가 손익
            RETURN_RATE = round(EVALUATE_RETURN / BID_PRICE * 100, 2) # 수익률
            
            asset[STSL].append(SYMBOL)
        
            asset[STIL][SYMBOL] = {
                "MARKET_PRICE" : MARKET_PRICE,
                "AVERAGE_PRICE" : AVERAGE_PRICE,
                "HOLDING_BALANCE" : HOLDING_BALANCE,
                "BID_PRICE" : BID_PRICE,
                "EVALUATE_PRICE" : EVALUATE_PRICE,
                "EVALUATE_RETURN" : EVALUATE_RETURN,
                "RETURN_RATE" : f"{RETURN_RATE}%"
            }
            
        return asset
    
    
    def extract_portfolio(self, cooked_asset: list) -> dict:
        TOTAL_BID_PRICE = 0
        TOTAL_EVALUATE_PRICE = 0
        TOTAL_RETURN_PRICE = 0
    
        KRW = cooked_asset["KRW"]

        for STOCKED_TICKER_SYMBOL in cooked_asset["STOCKED_TICKER_SYMBOL_LIST"]:
            STOCKED_TICKER_INFO = cooked_asset["STOCKED_TICKER_INFO_LIST"][STOCKED_TICKER_SYMBOL]
            
            TOTAL_BID_PRICE = TOTAL_BID_PRICE + STOCKED_TICKER_INFO["BID_PRICE"]
            TOTAL_EVALUATE_PRICE = TOTAL_EVALUATE_PRICE + STOCKED_TICKER_INFO["EVALUATE_PRICE"]
            TOTAL_RETURN_PRICE = TOTAL_RETURN_PRICE + STOCKED_TICKER_INFO["EVALUATE_RETURN"]
    
        portfolio = {
            "TOTAL_ASSET" : KRW + TOTAL_EVALUATE_PRICE,
            "TOTAL_BID_PRICE" : TOTAL_BID_PRICE,
            "TOTAL_EVALUATE_PRICE" : TOTAL_EVALUATE_PRICE,
            "TOTAL_RETURN_PRICE" : TOTAL_RETURN_PRICE,
            "TOTAL_RETURN_RATE" : f"{round(TOTAL_RETURN_PRICE / TOTAL_BID_PRICE * 100, 2)}%"
        }
        
        return portfolio
    
    
    def create_dashboard(self, cooked_asset: list[dict], portfolio: list) -> list[dict]:
        cooked_asset["PORTFOLIO"] = portfolio
        
        for STOCKED_TICKER_SYMBOL in cooked_asset["STOCKED_TICKER_SYMBOL_LIST"]:
            STOCKED_TICKER_INFO = cooked_asset["STOCKED_TICKER_INFO_LIST"][STOCKED_TICKER_SYMBOL]
            
            WEIGHT = round(STOCKED_TICKER_INFO["EVALUATE_PRICE"] / portfolio["TOTAL_ASSET"], 4) * 100
            
            STOCKED_TICKER_INFO["WEIGHT"] = f"{WEIGHT: .2f}%"
            
        return cooked_asset
