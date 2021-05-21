import pandas as pd
import numpy as np


def get_invoice(inn, number):
    sales = pd.read_excel('invoice.xls')

    b =sales.query(f'ИНН == {inn}').query(f'Номер == {int(number)}')
    a = [len(sales.query(f'ИНН == {inn}')), sales.loc[b.index].values[0][3], sales.loc[b.index].values[0][1]]

    return a
