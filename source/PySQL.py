import pymysql

class SQL:
    def __init__(self, connector: dict):
        self.connect = pymysql.connect(
        host="localhost",
        user="root",
        password=connector["PASSWORD"],
        db=connector["DATABASE"],
        charset="utf8"
    )
        
        
    def insert_to_asset(self, dashboard : list[dict]) -> None:
        portfolio = dashboard["PORTFOLIO"]
        
        curs = self.connect.cursor()
        
        curs.execute("select count(*) from asset;")
        
        if curs.fetchall()[0][0] == 0:
            delta_total_return_rate = "0.00%"
        else:
            curs.execute("SELECT total_return_rate FROM asset ORDER BY update_time DESC LIMIT 1;")
            
            delta_total_return_rate = float(portfolio["TOTAL_RETURN_RATE"][:-1]) - float(curs.fetchall()[0][0][:-1])
            
            if delta_total_return_rate > 0:
                delta_total_return_rate = f"+{delta_total_return_rate: .2f}%".replace(" ", "")
            else:
                delta_total_return_rate = f"{delta_total_return_rate: .2f}%".replace(" ", "")
                
        if portfolio["TOTAL_RETURN_RATE"][0] != "-":
            total_return_rate = f"+{portfolio['TOTAL_RETURN_RATE']}"
        else:
            total_return_rate = portfolio["TOTAL_RETURN_RATE"]
            
        sql = "INSERT INTO asset VALUES (%s, %s, %s, %s, %s, %s, %s, now());"
        set = (
            portfolio["TOTAL_ASSET"],
            dashboard["KRW"],
            portfolio["TOTAL_BID_PRICE"],
            portfolio["TOTAL_EVALUATE_PRICE"],
            portfolio["TOTAL_RETURN_PRICE"],
            total_return_rate,
            delta_total_return_rate
        )
        
        curs.execute(sql, set)
        
        self.connect.commit()


    def insert_to_history(self, dashboard : list[dict]) -> None:
        curs = self.connect.cursor()
        
        sql = "INSERT INTO history VALUES (%s, now());"
        set = (
            str(dashboard["STOCKED_TICKER_SYMBOL_LIST"])
        )
        
        curs.execute(sql, set)
        
        self.connect.commit()
        
        
    def insert_to_ticker(self, dashboard : list[dict]) -> None:
        curs = self.connect.cursor()

        curs.execute("SHOW TABLES;")
        
        tables = [i[0].upper() for i in curs.fetchall()]
        
        for STOCKED_TICKER_SYMBOL in dashboard["STOCKED_TICKER_SYMBOL_LIST"]:
            STOCKED_TICKER_INFO = dashboard["STOCKED_TICKER_INFO_LIST"][STOCKED_TICKER_SYMBOL]
            
            if STOCKED_TICKER_SYMBOL not in tables:
                sql = f'''
                        CREATE TABLE {STOCKED_TICKER_SYMBOL} (
                            holdings FLOAT(20, 8) DEFAULT 0.0,
                            bid_price FLOAT(10, 4) DEFAULT 0.0,
                            market_price FLOAT(15, 4) DEFAULT 0.0,
                            evaluate_price FLOAT(10, 4) DEFAULT 0.0,
                            evaluate_return INT DEFAULT 0,
                            return_rate VARCHAR(50) DEFAULT "0%",
                            weight VARCHAR(10) DEFAULT "0%",
                            delta_return_rate VARCHAR(50) DEFAULT "0%",
                            update_time DATETIME NOT NULL,
                            PRIMARY KEY(update_time)
                            );
                        '''
                        
                print(f"============= {STOCKED_TICKER_SYMBOL} TABLE CREATED =============")
                print(f"Executed SQL: {sql}")
                
                curs.execute(sql)
                
                self.connect.commit()
                
            curs = self.connect.cursor()
            
            curs.execute(f"SELECT count(*) FROM {STOCKED_TICKER_SYMBOL};")
                    
            if curs.fetchall()[0][0] == 0:
                delta_return_rate = "0.00%"
            else:
                curs.execute(f"SELECT return_rate FROM {STOCKED_TICKER_SYMBOL} ORDER BY update_time DESC LIMIT 1;")
                
                delta_return_rate = float(STOCKED_TICKER_INFO["RETURN_RATE"][:-1]) - float(curs.fetchall()[0][0][:-1])
                
                if delta_return_rate > 0:
                    delta_return_rate = f"+{delta_return_rate: .2f}%".replace(" ", "")
                else:
                    delta_return_rate = f"{delta_return_rate: .2f}%".replace(" ", "")
                    
            if STOCKED_TICKER_INFO["RETURN_RATE"][0] != "-":
                return_rate = f"+{STOCKED_TICKER_INFO['RETURN_RATE']}"
            else:
                return_rate = STOCKED_TICKER_INFO["RETURN_RATE"]
                    
            sql = f"INSERT INTO {STOCKED_TICKER_SYMBOL} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now());"
            set = (
                STOCKED_TICKER_INFO["HOLDING_BALANCE"],
                STOCKED_TICKER_INFO["BID_PRICE"],
                STOCKED_TICKER_INFO["MARKET_PRICE"],
                STOCKED_TICKER_INFO["EVALUATE_PRICE"],
                STOCKED_TICKER_INFO["EVALUATE_RETURN"],
                return_rate,
                STOCKED_TICKER_INFO["WEIGHT"],
                delta_return_rate
            )
            
            curs.execute(sql, set)
    
            self.connect.commit()
            
            
    def destroy(self):
        self.connect.close()