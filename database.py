import sqlite3


db = sqlite3.connect('infobot.db')
cur = db.cursor()
    # Создаем таблицу
cur.execute("""CREATE TABLE IF NOT EXISTS usersinfo (
    id INT,
    userid TEXT,
    inn TEXT,
    activ BOOLEAN)""")

cur.execute("""CREATE TABLE IF NOT EXISTS invoice (
    INN INT,
    COMPANY TEXT,
    NUMBER INT,
    STATUS TEXT,
    Delivery TEXT,
    TC TEXT,
    SUMMA INT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS person (
    INN INT,
    COMPANY TEXT,
    NUMBER INT,
    STATUS TEXT,
    Delivery TEXT,
    TC TEXT,
    SUMMA INT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS goods (
    INN INT,
    NUMBER INT,
    PRODUTC TEXT,
    AMOUNT INT,
    STATUS TEXT,
    DATESHIPMENT DATE)
    """)

cur.execute("""CREATE TABLE IF NOT EXISTS products (
    INN INT,
    NUMBER INT,
    PRODUTC TEXT,
    AMOUNT INT,
    STATUS TEXT,
    DATESHIPMENT DATE)
    """)
db.commit()
db.close()

print('Выполнено')

