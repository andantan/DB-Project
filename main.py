import datetime
import requests
import sys

from time import sleep

import scripts.Upbit as upt
import scripts.PySQL as sql

from scripts.fnt import fnt_ConnectionError
from scripts.fnt import fnt_connected

key = {
    "ACCESS_KEY": "WVSh6xWB1UwrZmf3Q30f2hxHGnEyhN8nWXGtXRyx",
    "SECRET_KEY": "l2zsmJaagsd2qLIY8I8xw3bDzfcgrFsHpxQx6bMX"
}

mode = {
    "-d": 0,
    "-r": 1
}

upbit_API = upt.Upbit(keys=key)

def main(mode):
    if mode:
        upbit_SQL = sql.SQL()
        margin, i = 0, 1

        print("\n/- Query Start(" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ")\n")

        try:
            while True:
                now = datetime.datetime.now()

                if int(now.strftime('%S')) % 5 == 0:
                    try:
                        print(f"flag %5d | {now.strftime('%Y-%m-%d %H:%M:%S')}" % i, end=" ")

                        upbit_API.get_asset(file=False)

                        if margin != upbit_API.MARGIN:
                            if i != 1:
                                flag = upbit_API.MARGIN - margin

                                print(f"- Data updated({margin}% -> {upbit_API.MARGIN}%)")
                            else:
                                flag = "N/A"

                                print(f"- Data initialized(value = {upbit_API.MARGIN}%)")

                            upbit_SQL.insert_to_wallet(asset=upbit_API.ASSET, pp=flag)

                            margin = upbit_API.MARGIN
                        else:
                            print("- ignored")
                    
                        sleep(1)

                        i += 1

                    except requests.exceptions.ConnectionError:
                        fnt_ConnectionError(openIP=True)

                        print(f"/- Query restart({now.strftime('%Y-%m-%d %H:%M:%S')})")

                        sleep(10)
        except KeyboardInterrupt:
            print("\n" + f"/- Keyboard inturrupted(request terminated) - flag {i} times tried\n")
        finally:
            upbit_SQL.destroy()
    else:
        upbit_API.get_asset(file=True)

if __name__ == '__main__':
    if fnt_connected():
        main(mode[sys.argv[1]])
    else:
        print("Please check network condition.")
