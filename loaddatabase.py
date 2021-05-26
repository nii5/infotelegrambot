import pandas as pd
import sqlite3
import time

db = sqlite3.connect('infobot.db')

while True:
    sales = pd.read_excel('/mnt/blackhorse/invoice.xlsx')
    cur = db.cursor()
    cur.execute('DELETE FROM invoice')
    sales.to_sql('invoice', con=db, if_exists='append', index=False)
    db.commit()

    products = pd.read_excel('/mnt/blackhorse/product.xlsx')
    cur = db.cursor()
    cur.execute('DELETE FROM products')
    products.to_sql('products', con=db, if_exists='append', index=False)
    db.commit()

    sales = pd.read_excel('/mnt/blackhorse/person.xlsx')
    cur = db.cursor()
    cur.execute('DELETE FROM person')
    sales.to_sql('person', con=db, if_exists='append', index=False)
    db.commit()

    products = pd.read_excel('/mnt/blackhorse/goods.xlsx')
    cur = db.cursor()
    cur.execute('DELETE FROM goods')
    products.to_sql('goods', con=db, if_exists='append', index=False)
    db.commit()
    print("Выполнено")
    time.sleep(14400)
