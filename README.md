# DB-Project
Database project respository

테이블 생성 script

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

============================================================================

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

============================================================================
변경된 테이블 생성 Script

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
