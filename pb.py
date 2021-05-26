import pandas as pd
import sqlite3
db = sqlite3.connect('infobot.db')
# sales = pd.read_excel('invoice.xlsx')
# cur = db.cursor()
# cur.execute('DELETE FROM invoice')
# sales.to_sql('invoice', con=db, if_exists='append', index=False)


def get_invoice(inn, number):
    query = f'SELECT * FROM invoice WHERE INN={inn} AND NUMBER={number}'
    sales = pd.read_sql(query, con=db)
    if not sales.empty:
        return sales.values.tolist()
    else:
        return False

def get_invoice_person( number):
    query = f'SELECT * FROM person WHERE NUMBER={number}'
    sales = pd.read_sql(query, con=db)
    if not sales.empty:
        return sales.values.tolist()
    else:
        return False


def get_products(inn, number):
    query = f'SELECT PRODUTC, AMOUNT, STATUS FROM products WHERE INN={inn} AND NUMBER={number}'
    products = pd.read_sql(query, con=db)
    if not products.empty:
        products = products.rename({'PRODUTC': 'Номенклатура', 'AMOUNT': 'Колво', 'STATUS': 'Статус'}, axis='columns')
        return products
    else:
        return False


def get_goods(number):
    query = f'SELECT PRODUTC, AMOUNT, STATUS FROM goods WHERE NUMBER={number}'
    products = pd.read_sql(query, con=db)
    if not products.empty:
        products = products.rename({'PRODUTC': 'Номенклатура', 'AMOUNT': 'Колво', 'STATUS': 'Статус'}, axis='columns')
        return products
    else:
        return False


def save_users(userid):

    query = f'INSERT INTO usersinfo (userid, inn, activ) VALUES ({userid}, {0}, {True});'
    cur = db.cursor()
    cur.execute(query)
    db.commit()


def get_all_users():

    query = f'SELECT userid FROM usersinfo'
    users = pd.read_sql(query, con=db)
    return users.values.tolist()



def find_user(userid):
    query = f'SELECT userid, inn FROM usersinfo WHERE userid={userid}'
    user = pd.read_sql(query, con=db)
    if not user.empty:
        return user.values.tolist()
    else:
        save_users(userid)
        return [[userid, 0]]


def save_users_inn(userid, userinn):
    query = f'Update usersinfo set inn = {userinn} where userid = {userid};'
    cur = db.cursor()
    cur.execute(query)
    db.commit()


# a = np.delete(a, 0, axis=0)
# np.save(f'userid', a)
# save_users(164497703)
# save_users_inn(164497703, 4501008142)
# find_user(164497703)
#
# # a = np.load('userid.npy')
# print(get_all_users())
#
# print(get_invoice(4501008142, 3647))