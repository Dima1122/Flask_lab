from app import app
import pandas as pd
import numpy as np
import scipy.stats as st
import sqlite3
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import wget
import zipfile
import os
from matplotlib.patches import Ellipse
import math
import matplotlib.transforms as transforms
import matplotlib.pyplot as plt

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

def get_all_data():
    try:
        conn = sqlite3.connect('C:/Users/User/Documents/Спец_БД/Lab_4/Flask_lab/app.sqlite')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sqlite_select_query = """SELECT * from wine"""
        cursor.execute(sqlite_select_query)
        col_name_list = [tuple[0] for tuple in cursor.description]
        records = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        conn.close()
        
    data = pd.DataFrame(records, columns = col_name_list)
    return data

def confidence_ellipse(x,y,ax,p_value, facecolor = 'none', **kwargs):
    if x.size != y.size:
        raise ValueError('error')
    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0,0] * cov[1, 1])
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0,0), width = ell_radius_x * 2, height = ell_radius_y * 2,
                      facecolor = facecolor, **kwargs)
    n_std = math.sqrt(-2 * math.log(p_value))
    scale_x = np.sqrt(cov[0,0])*n_std
    mean_x = np.mean(x)
    scale_y = np.sqrt(cov[1,1]) * n_std
    mean_y = np.mean(y)
    transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(mean_x, mean_y)
    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)


def get_coordinates(field1, field2, scale):
    data = get_data(field1, field2)
    fig, ax = plt.subplots(figsize=(8,8))
    confidence_ellipse(data[field1], data[field2], ax, scale, edgecolor='green')
    ax.scatter(data[field1], data[field2], s = 10)
    plt.title('Predictive ellipsis')
    plt.xlabel(field1)
    plt.ylabel(field2)
    my_path = os.path.dirname(os.path.abspath(__file__))
    fig.savefig(my_path + '\\..\\app\\static\\'+field1+'_'+field2+'.svg')
    plt.close(fig)
    return '../static/'+field1+'_'+field2+'.svg'
    

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
        attr_and_info.append(('PS'+str(i), eigenvalues[i], pca.explained_variance_ratio_[i], np.around(eigenvectors[i], decimals = 4)))
    return get_important_components(attr_and_info)


def calculate_pca():
    data = get_all_data()
    components = get_PCA(data)
    return components



















