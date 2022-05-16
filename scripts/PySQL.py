import pymysql

class SQL:
    def __init__(self):
        self.connect = pymysql.connect(
        host="localhost",
        user="root",
        password="wjsrbqls123!",
        db="asset",
        charset="utf8"
    )

    def insert_to_wallet(self, asset, pp):
        percent_point = "0"

        if type(pp) == float:
            if 0 < pp:
                percent_point = f"+{round(pp, 2)}%p"
            else:
                percent_point = f"{round(pp, 2)}%p"
        else:
            percent_point = pp
        
        portfolio = asset["portfolio"]

        curs = self.connect.cursor()

        sql = "INSERT INTO wallet VALUES (%s, %s, %s, %s, %s, %s, %s, now())"

        curs.execute(sql, (
            portfolio["total_asset"],
            portfolio["KRW"],
            portfolio["total_blended_price"],
            portfolio["total_market_price"],
            portfolio["total_return"],
            portfolio["margin_average"],
            percent_point
        ))

        self.connect.commit()

    def destroy(self):
        self.connect.close()
