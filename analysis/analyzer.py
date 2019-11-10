import pandas as pd
import numpy as np
import scipy.stats
from app import app
import sqlite3
import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr
rpy2.robjects.numpy2ri.activate()


def get_data():
    try:
        conn = sqlite3.connect('C:/Users/User/Documents/Спец_БД/Lab_4/Flask_lab/app.sqlite')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sqlite_select_query = """SELECT * from observation where id<=2139"""
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

def get_contingency_table(field1: str, field2: str):
    '''
    :param field1:
    :param field2:
    :return: таблица сопряженности
    '''
    data = get_data()
    crosstab = pd.crosstab(data[field1],data[field2],margins = True)
    horizontal_names = [crosstab.columns.name] + list(crosstab.columns)
    vertical_names = [crosstab.index.name] + list(crosstab.index)
    values = list(crosstab.values)
    return [horizontal_names, vertical_names, values]


def get_expected_table(field1: str, field2: str):
    '''
        :param field1:
        :param field2:
        :return: таблица ожидаемых значений
    '''
    data = get_data()
    crosstab = pd.crosstab(data[field1],data[field2],margins = True)
    expected = scipy.stats.contingency.expected_freq(crosstab)
    horizontal_names = [crosstab.columns.name] + list(crosstab.columns)
    vertical_names = [crosstab.index.name] + list(crosstab.index)
    values = list(expected)
    return [horizontal_names, vertical_names, values]

def choose_method(crosstab):
    '''
        :param crosstab
        :return: statistic_name
    '''
    if (crosstab.shape[0]<= 2 and crosstab.shape[1]<=2):
        if np.all(crosstab > 10):
            return 'chi-square-pearson'
        elif np.all(crosstab > 4):
            return 'chi-cquare-yetes-correction'
        else:
            return 'fischer-exact'
    elif (crosstab[np.where(crosstab < 5)].shape[0] / (crosstab.shape[0] * crosstab.shape[1]) < 0.2):
        return 'chi-square-pearson'
    elif crosstab.sum() < 500:
        return 'freeman-colton'
    return 'freeman-colton-with-monte-carlo'

def get_statistic(field1, field2):
    '''
        :param field1:
        :param field2:
        :return: таблица ожидаемых значений
    '''
    data = get_data()
    crosstab = pd.crosstab(data[field1],data[field2],margins = True)
    expected = scipy.stats.contingency.expected_freq(crosstab)
    method = choose_method(expected)
    if method == 'chi-square-pearson':
        chi2, p_value, dof, expected = scipy.stats.chi2_contingency(crosstab, correction = False)
        return 'chi-square-pearson', p_value
    if method == 'chi-square-yetes-correction':
        chi2, p_value, dof, expected = scipy.stats.chi2_contingency(crosstab, correction = True)
        return 'chi-square-yetes-correction', p_value
    if method == 'fischer-exact':
        oddsratio, p_value = scipy.stats.fisher_exact(crosstab)
        return 'fisher-exact', p_value
    if method == 'freeman-colton':
        stats = importr('stats')
        m = np.array(crosstab.values)
        res = stats.fisher_test(m)
        return 'freeman-colton', res[0]
    if method == 'freeman-colton-with-monte-carlo':
        stats = importr('stats')
        m = np.array(crosstab.values)
        res = stats.fisher_test(m, simulate_p_value = True, B = m.sum()*10)
        return 'freeman-colton-with-monte-carlo', float(list(res[0])[0])
    return 'oops, something went wrong'