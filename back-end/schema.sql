DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS tradesman;
DROP TABLE IF EXISTS rider;
DROP TABLE IF EXISTS goods;


CREATE TABLE customer (
    name TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL,
    telephone TEXT NOT NULL,
    birthday TEXT,
    gender INTEGER,
    realname TEXT NOT NULL,
    id TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE tradesman (
    name TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL,
    telephone TEXT NOT NULL,
    address TEXT NOT NULL,
    storename TEXT NOT NULL
);

CREATE TABLE rider (
    name TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL,
    telephone TEXT NOT NULL,
    realname TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE goods (
    storename TEXT NOT NULL,
    goodsname TEXT NOT NULL,
    price REAL NOT NULL,
    PRIMARY KEY(storename, goodsname)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status INTEGER NOT NULL,
    customer TEXT NOT NULL,
    rider TEXT,
    storename TEXT NOT NULL,
    goodsname TEXT NOT NULL,
    number INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (customer) REFERENCES customer (name),
    FOREIGN KEY (rider) REFERENCES rider (name),
    FOREIGN KEY (storename, goodsname) REFERENCES goods (storename, goodsname)
);