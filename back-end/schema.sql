DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS tradesman;
DROP TABLE IF EXISTS rider;
DROP TABLE IF EXISTS goods;
DROP TABLE IF EXISTS basic_order;
DROP TABLE IF EXISTS detailed_order;

CREATE TABLE customer (
    name TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL,
    telephone TEXT NOT NULL,
    birthday TEXT,
    gender TEXT,
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
    id TEXT NOT NULL,
    address TEXT NOT NULL
);

CREATE TABLE goods (
    storename TEXT NOT NULL,
    goodsname TEXT NOT NULL,
    price REAL NOT NULL,
    PRIMARY KEY(storename, goodsname),
    FOREIGN KEY (storename) REFERENCES tradesman (storename)
);

CREATE TABLE basic_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status INTEGER NOT NULL,
    customer TEXT NOT NULL,
    rider TEXT,
    FOREIGN KEY (customer) REFERENCES customer (name),
    FOREIGN KEY (rider) REFERENCES rider (name)
);

CREATE TABLE detailed_order (
    id INTEGER PRIMARY KEY NOT NULL,
    storename TEXT NOT NULL,
    goodsname TEXT NOT NULL,
    number INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (storename, goodsname) REFERENCES goods (storename, goodsname),
    FOREIGN KEY (id) REFERENCES basic_order (id)
);