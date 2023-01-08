import sqlite3
import os

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




