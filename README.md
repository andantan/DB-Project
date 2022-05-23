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
