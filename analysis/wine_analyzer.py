from app import app
import pandas as pd
import numpy as np
import scipy.stats as st
import sqlite3

def get_data(field1, field2):
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    data = cursor.execute('SELECT ' + field1 + ',' + field2 + ' FROM WINE').fetchall()
    conn.close()
    return pd.DataFrame(data, columns=[field1,field2])

def get_all_data(cols):
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    data = cursor.execute('SELECT * FROM WINE').fetchall()
    conn.close()
    return pd.DataFrame(data, columns=cols)

def get_coordinates(field1,  field2):
    data = get_data(field1, field2)

    #расчёт координат эллипса

    return svg


def calculate_pca(cols):
    data = get_all_data(cols)
    #находим главные компоненты, объясняющие 95% дисперсии
    return components