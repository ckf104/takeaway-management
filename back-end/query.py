import sqlite3
import os
from datetime import datetime, timedelta

db = sqlite3.connect(f'{os.path.dirname(__file__)}/database.db')
db.row_factory = sqlite3.Row

fetch1 = db.execute(
    'SELECT customer, count(*) FROM orders WHERE order_time > ? GROUP BY customer ORDER BY count(*) DESC, customer ASC LIMIT 10',
    ('2021-01-01 23:59:59',),
).fetchall()
print("Q1----------------------------------")
for row in fetch1 :
    print(f"customer: {row[0]}, count: {row[1]}")

fetch2 = db.execute(
    'SELECT storename, count(*) FROM orders GROUP BY storename ORDER BY count(*) DESC, sum(number*price) DESC LIMIT 1'
).fetchone()
print("Q2----------------------------------")
print(f"storename: {fetch2[0]}, consumption: {fetch2[1]}")

days_ago = datetime.today() - timedelta(days=30)
order_time_min = days_ago.strftime("%Y-%m-%d") + " 23:59:59"
fetch3 = db.execute(
    "SELECT storename FROM orders WHERE order_time > ? \
     GROUP BY storename \
     HAVING count(id) < \
         (SELECT avg(num) FROM \
             (SELECT count(id) AS num FROM orders WHERE order_time > ? GROUP BY storename))",
    (order_time_min, order_time_min)
).fetchall()
print("Q3-----------------------------------")
if len(fetch3) == 0 :
    print("no orders in 30 days")
else :
    for row in fetch3 :
        print(f'storename: {row[0]}')

days_ago = datetime.today() - timedelta(days=10000)
order_time_min = days_ago.strftime("%Y-%m-%d") + " 23:59:59"
fetch4 = db.execute(
    'SELECT storename, goodsname FROM orders\
     WHERE order_time > ?\
     GROUP BY storename, goodsname\
     HAVING sum(number*price) =\
         (SELECT min(s) FROM\
            (SELECT sum(number*price) AS s FROM orders WHERE order_time > ? GROUP BY storename, goodsname)\
         )',
    (order_time_min, order_time_min)
).fetchall()
print("Q4------------------------------------")
if len(fetch4) == 0 :
    print("no orders in 7 days")
else :
    for row in fetch4 :
        print(f'storename: {row[0]}, goodsname: {row[1]}')


