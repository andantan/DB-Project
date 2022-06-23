from upbit import Upbit
from PySQL import SQL

import datetime

from time import sleep
from pprint import pprint

API_KEY = {
    "ACCESS_KEY" : "LAxtuQAXYD0kb79FksZxIHTt85lL9UwLdbTN9j9Z",
    "SECRET_KEY" : "VMocgGBMrwVU7f3wws8en06LbfiaxuCqXFJqxQZb", # IP related Key
}

MYSQL_CONNECTOR = {
    "PASSWORD" : "1234!",
    "DATABASE" : "upbit"
}

PyUpbit = Upbit(API_KEY)
PySQL = SQL(MYSQL_CONNECTOR)


if __name__ == '__main__':
    print("\n/- Query Start(" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ")", end="\n\n")
    
    i = 0
    
    try:
        while True:
            now = datetime.datetime.now()

            if int(now.strftime('%S')) % 5 == 0:
                try:
                    print(f"\n\033[95m Query %5d \033[96m | {now.strftime('%Y-%m-%d %H:%M:%S')}\033[0m" % i, end="\n\n")
                    
                    raw_asset = PyUpbit.request_asset()
                    cooked_asset = PyUpbit.cooking_raw_wallet(raw_asset=raw_asset)
                    portfolio = PyUpbit.extract_portfolio(cooked_asset=cooked_asset)
                    dashboard = PyUpbit.create_dashboard(cooked_asset=cooked_asset, portfolio=portfolio)

                    PySQL.insert_to_asset(dashboard=dashboard)
                    PySQL.insert_to_history(dashboard=dashboard)
                    PySQL.insert_to_ticker(dashboard=dashboard)
                    
                    pprint(dashboard, indent=4)
                    
                    sleep(1)

                    i += 1
                except:
                    print(f"/- Query restart({now.strftime('%Y-%m-%d %H:%M:%S')})")

                    sleep(10)
    except KeyboardInterrupt:
        print("\n" + f"/- Keyboard inturrupted(request terminated) - flag {i} times tried\n")
    finally:
        SQL.destroy()
