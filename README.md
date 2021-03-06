# DB-Project
Database project respository

테이블 생성 초기 script

CREATE TABLE `api_key` (  
  `PUBLIC_KEY` varchar(150) NOT NULL,  
  `SECRET_KEY` varchar(150) NOT NULL,  
  PRIMARY KEY (`SECRET_KEY`)  
);  
  
CREATE TABLE `asset` (  
  `보유KRW` int DEFAULT '0',  
  `총매수금액` int DEFAULT '0',  
  `총평가금액` int DEFAULT '0',  
  `평가손익` int DEFAULT '0',  
  `수익률` int DEFAULT '0',  
  `포트폴리오` varchar(250) DEFAULT NULL,  
  `갱신시각` datetime NOT NULL,  
  PRIMARY KEY (`갱신시각`)  
);  
  
CREATE TABLE `portfolio` (  
  `코인이름` varchar(50) NOT NULL,  
  `SYMBOL` varchar(50) NOT NULL,  
  `평가손익` int DEFAULT '0',  
  `수익률` int DEFAULT '0',  
  `보유수량` int DEFAULT '0',   
  `매수평균가` int DEFAULT '0',  
  `평가금액` int DEFAULT '0',  
  `매수금액` int DEFAULT '0',  
  `현재가` int DEFAULT '0',  
  `갱신시각` datetime NOT NULL,  
  `비중` int DEFAULT '0',  
  `페어` varchar(50) DEFAULT 'KRW',  
  PRIMARY KEY (`갱신시각`)  
);  
  
CREATE TABLE `history` (  
  `갱신시각` datetime NOT NULL,  
  `수익률` int DEFAULT '0',  
  `증감률` int DEFAULT '0',  
  `총보유자산` int DEFAULT '0',  
  `포트폴리오` varchar(250) DEFAULT NULL,  
  PRIMARY KEY (`갱신시각`)  
);  
  
CREATE TABLE `component_history` (  
  `SYMBOL` varchar(50) NOT NULL,  
  `갱신시각` datetime NOT NULL,  
  `수익률` int DEFAULT '0',  
  `증감률` int DEFAULT '0',  
  `현재가` int DEFAULT '0',  
  PRIMARY KEY (`갱신시각`)  
);  
  
===========================================================================  
  
(2022-06-22 이전)  
Asset 테이블을 부모테이블이라 하면 portfolio, history, component_history의 기본기인 갱신시각은 모두 Asset 테이블의 갱신시각을 외래키로 지정할 수 있다.  
따라서 Asset을 제외한 portfolio, history, component_history테이블에  
  #forien key("갱신시각") references asset("갱신시각")  
구문을 추가하여야한다.  
하지만, 사용자가 특정 기간동안의 데이터를 삭제하고자 할 때는 Asset의 갱신시각을 Where 구문에 대입함으로써 자식 테이블인 portfolio, history, component_history의 데이터를 동시에 삭제해야한다.  
따라서 On delete 옵션을 cascade로 지정하여야 하므로,  
  #forien key("갱신시각") references asset("갱신시각") on delete cascade  
구문으로 추가하여야한다.  
투자한 Stock에 대한 데이터는 삭제만 가능하고 변경은 불가능하므로 on update는 신경쓰지 않아도 된다.  
갱신시각을 제외한 모든 개체들은 독립적이고, 각 테이블의 모든 결정자가 "갱신시각"이고, 이는 후보키이므로 BCNF 정규형에 속한다.  
  
변경 (2022-06-22)  
  
모든 테이블에서 외래키는 필요하지 않으므로 제거 및 갱신시각 하나만으로 모든 속성들을 하나로 결정할 수 있으므로 갱신 릴레이션에 갱신 시각을 추가한다.  
모든 속성의 도메인이 원자값으로만 구성되므로 제 1정규형을 만족한다.  
모든 속성이 기본키에 완전 함수 종속되어 모든 Entity의 모든 속성이 갱신시각 단 하나만으로 결정되므로 제 2 정규형을 만족한다.  
모든 속성이 이행적 함수 종속을 만족하지 않으므로 제 3 정규형을 만족한다.  
모든 개체의 속성이 단 하나의 후보키인 갱신시각으로 결정되므로 보이스/코드 정규형을 만족한다.  
  
===========================================================================  
  
변경된 테이블 생성 Script (2022-06-22 이전, 외래키 존재)  
  
CREATE TABLE `portfolio` (  
  `코인이름` varchar(50) NOT NULL,  
  `SYMBOL` varchar(50) NOT NULL,  
  `평가손익` int DEFAULT '0',  
  `수익률` int DEFAULT '0',  
  `보유수량` int DEFAULT '0',  
  `매수평균가` int DEFAULT '0',  
  `평가금액` int DEFAULT '0',  
  `매수금액` int DEFAULT '0',  
  `현재가` int DEFAULT '0',  
  `갱신시각` datetime NOT NULL,  
  `비중` int DEFAULT '0',  
  `페어` varchar(50) DEFAULT 'KRW',  
  PRIMARY KEY (`갱신시각`)  
  forien key("갱신시각") references asset("갱신시각") on delete cascade  
);  
  
CREATE TABLE `history` (  
  `갱신시각` datetime NOT NULL,  
  `수익률` int DEFAULT '0',  
  `증감률` int DEFAULT '0',  
  `총보유자산` int DEFAULT '0',  
  `포트폴리오` varchar(250) DEFAULT NULL,  
  PRIMARY KEY (`갱신시각`)  
  forien key("갱신시각") references asset("갱신시각") on delete cascade  
);  
  
CREATE TABLE `component_history` (  
  `SYMBOL` varchar(50) NOT NULL,  
  `갱신시각` datetime NOT NULL,  
  `수익률` int DEFAULT '0',  
  `증감률` int DEFAULT '0',  
  `현재가` int DEFAULT '0',  
  PRIMARY KEY (`갱신시각`)  
  forien key("갱신시각") references asset("갱신시각") on delete cascade  
);  

===========================================================================  

변경 (2022-06-22 외래케 제거 및 정규화 완료)

create table API_KEY(  
        PUBLIC_KEY VARCHAR(100) NOT NULL,  
        SECRET_KEY VARCHAR(100) NOT NULL,  
        PRIMARY KEY(SECRET_KEY)  
        );  
  
create table ASSET (  
       total_asset INT DEFAULT 0,  
       KRW INT DEFAULT 0,  
       total_purchase_amount INT DEFAULT 0,  
       total_evaluate_amount INT DEFAULT 0,  
       total_return_amount INT DEFAULT 0,  
       total_return_rate VARCHAR(50) DEFAULT "0%",  
       update_time DATETIME NOT NULL,  
       PRIMARY KEY(update_time)  
       );

 CREATE TABLE TICKER_FORM (
       holdings FLOAT(20, 8) DEFAULT 0.0,  
       bid_price FLOAT(10, 4) DEFAULT 0.0,  
       market_price FLOAT(50, 4) DEFAULT 0.0,  
       evaluate_price FLOAT(10, 4) DEFAULT 0.0,  
       evaluate_return INT DEFAULT 0,  
       return_rate VARCHAR(50) DEFAULT "0%",  
       weight VARCHAR(10) DEFAULT "0%",  
       delta_return_rate VARCHAR(50) DEFAULT "0%",  
       update_time DATETIME NOT NULL,  
       PRIMARY KEY(update_time)  
       );  
 => 매매 릴레이션의 포트폴리오의 SYMBOL 구성요소들 중   
      해당 SYMBOL 테이블이 존재할 시 데이터 삽입, 존재하지 않을 시 테이블 생성  
      ex) 매매.포트폴리오 = (BTC, ETH, XRP) 일 때 XRP 테이블만 존재할 시   
           BTC, ETH 테이블 생성 후 각각 시장 데이터 조회 후 데이터 삽입  
           
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
                
  
CREATE TABLE history(  
       portfolio VARCHAR(500) DEFAULT "()",  
       update_time DATETIME NOT NULL,  
       PRIMARY KEY(update_time)  
       );  
       
===========================================================================  
    
![1](https://user-images.githubusercontent.com/75199215/175197130-8a116a97-0404-4a25-a626-9759a82ddc40.png)

===========================================================================  
  
릴레이션  
API_Key 릴레이션(Public_Key, Secret_Key(PRI))  
자산 릴레이션(총수익률, 총평가금액, 총매수금액, 총보유자산, 총평가손익, 보유KRW, 수익변화율, 갱신시각(PRI))  
매매 릴레이션(포트폴리오, 갱신시각(PRI))  
Ticker 릴레이션(수익률, 현재가, 보유개수, 평가손익, 매수금액, 평가금액, 비중, 수익변화율, 갱신시각(PRI))  
    -> 매매 릴레이션의 포트폴리오의 SYMBOL 구성요소들 중 해당 SYMBOL 테이블이 존재할 시 데이터 삽입, 존재하지 않을 시 테이블 생성  
portfolio 릴레이션(포트폴리오, 갱신시각(PRI))  
  
