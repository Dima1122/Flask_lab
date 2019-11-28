from app import app
import pandas as pd
import numpy as np
import scipy.stats as st
import sqlite3
import wget
import zipfile
import os

def update():
    url = 'https://sci2s.ugr.es/keel/dataset/data/classification/winequality-red.zip'
    wget.download(url)
    z = zipfile.ZipFile('winequality-red.zip', 'r')
    z.extractall()
    z.close()
    datContent = [i.strip().split() for i in open('winequality-red.dat').readlines()]
    attributes = [x[1] for x in datContent if x[0] == '@attribute']
    attributes[len(attributes) - 1] = 'Quality'
    data_tmp = datContent[16:]
    data = []
    for row in data_tmp:
        data.append([float(x) for x in row[0].split(',')])
    df = pd.DataFrame(data, columns=attributes)
    conn = sqlite3.connect(app.config['DATABASE'])
    df.to_sql('WINE', con=conn, if_exists='append', index=False)
    conn.commit()
    conn.close()
    os.remove('winequality-red.zip')
    os.remove('winequality-red.dat')
    return

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
