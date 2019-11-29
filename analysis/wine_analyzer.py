from app import app
import pandas as pd
import numpy as np
import scipy.stats as st
import sqlite3
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

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

def standartize(data):
    scaler = StandardScaler()
    X = data.drop('Quality', axis = 1)
    Y = data['Quality']
    X = scaler.fit(X).transform(X)
    return X,Y

def get_important_components(components):
    summ = 0
    important_components = []
    for component in components:
        if summ >= 0.95:
            return important_components, summ
        summ += component[2]
        important_components.append(component)
    return important_components, summ

def get_PCA(data):    
    pca = PCA()
    X, Y = standartize(data)
    table_train = pca.fit_transform(X)
    cov = pca.get_covariance()
    [eigenvalues, eigenvectors] = np.linalg.eig(cov)
    attr_and_info = []
    for i in range(len(pca.explained_variance_ratio_)):
        attr_and_info.append((data.drop('Quality', axis = 1).columns[i], eigenvalues[i], pca.explained_variance_ratio_[i]))
    attr_and_info_sorted = sorted(attr_and_info, key=lambda x: x[2], reverse = True)
    return get_important_components(attr_and_info_sorted)


def calculate_pca(cols):
    data = get_all_data(cols)
    components = get_PCA(data)
    return components



















