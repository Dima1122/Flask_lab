# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:49:07 2019

@author: User
"""
from app import app
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import scipy.stats as st
from statsmodels.formula.api import ols
from statsmodels.stats import anova
from scipy.stats import anderson
from statsmodels.stats.stattools import durbin_watson
import sqlite3
import os

def get_data():
    try:
        conn = sqlite3.connect(app.config['DATABASE'])
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sqlite_select_query = """SELECT EmploymentStatus,Gender,HasDebt,CityPopulation,
        JobWherePref,JobPref,SchoolDegree,MaritalStatus,Income from observation where id<=753"""
        cursor.execute(sqlite_select_query)
        col_name_list = [tuple[0] for tuple in cursor.description]
        records = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        conn.close()
    data = pd.DataFrame(records, columns=col_name_list)
    return data

def save_boxplot(data, factors):
    my_path = os.path.dirname(os.path.abspath(__file__))
    for factor in factors:
        _factors = factor.split('__')
        if len(_factors) == 1:
            labels = list(data[factor].unique())
            data_list = []
            for name in labels:
                data_list.append(data[data[factor] == name]['Income'])
            fig = plt.figure(figsize=(20, 10))
            plt.boxplot(data_list, labels = labels)
            plt.title(factor)
            fig.savefig(my_path+'\\..\\app\\static\\'+factor+'.png')
            plt.close(fig)
        else:    
            all_attributes = list(data.groupby(_factors).groups.keys())
            data_list = []
            for labels in all_attributes:
                tmp = data
                for i in range(len(labels)):
                    tmp = tmp[tmp[_factors[i]] == labels[i]]
                data_list.append(tmp['Income'])
            fig = plt.figure(figsize=(20, 10))
            plt.boxplot(data_list, labels = all_attributes)
            plt.xticks(rotation=90)
            plt.title(factor)
            fig.savefig(my_path+'\\..\\app\\static\\'+factor+'.png')
            plt.close(fig)

def check_normality(data):
    size = data.shape[0]
    if size < 2000:
        p_value = st.shapiro(data['Income'])[1]
        if p_value <= 0.05:
            return p_value, 'Not normal'
        else:
            return p_value, 'Normal'
    else:
        res = anderson(data['Income'])
        if res.statistic < res.critical_values[4]:
            return p_value, 'Normal'
        else:
            return p_value, 'Not normal'

def check_autocorrelation(residual):
    s = durbin_watson(residual)
    if s<=1.5:
        return s,'there is positive correlation'
    if s>=2.5:
        return s, 'there is negative correlation'
    if s<2.5 and s>=2.1:
        return s, 'there is a slight negative correlation'
    if s>1.5 and s<=1.9:
        return s, 'there is a slight positive correlation'
    else:
        return s, 'there is no correlation'

def anova_analysis(res):
    data = get_data()
    model = ols(res, data)
    results = model.fit()
    p_value_norm, distribution = check_normality(data)
    if distribution == 'Not normal':
            data = data[:100]
            data['Income'] = data[['Income']].applymap(lambda x: np.log(x+1))
            q25, q75 = np.percentile(data['Income'], 25), np.percentile(data['Income'], 75)
            iqr = q75 - q25
            cut_off = iqr * 1.5
            lower, upper = q25 - cut_off, q75 + cut_off
            data = data[data['Income'] > lower]
            data = data[data['Income'] < upper]    
            info = '''We have reduced our data to dimension = 100 and took logarithm from income because 
                    there is no other way to make income normal'''
    p_value_norm, distribution = check_normality(data)
    model = ols(res, data)
    results = model.fit()
    results.summary()
    if distribution == 'Not Normal':
        return 'Sorry, data is terrible, we cannot perform anova analysis', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    anova_res = anova.anova_lm(results, typ=1, cache=True)
    anova_factors = anova_res[anova_res['PR(>F)'] < 0.1]['PR(>F)']
    factors = {}
    for i in range(len(anova_factors.index)):
        factor_name = anova_factors.index[i].replace('C(', '')
        factor_name = factor_name.replace(')', '')
        if ':' in factor_name:
            factor_name = factor_name.replace(':', '__')
        factors[factor_name] = anova_factors[i]         
    dw_stat, dw_decision = check_autocorrelation(results.resid.values)
    homoscedasticity, homoscedasticity_pv = results.diagn['omni'], results.diagn['omnipv']
    if homoscedasticity_pv > 0.05:
        homoscedasticity_decision = 'there is no homescedasticity and we may believe observed results'
    else:
        homoscedasticity_decision = 'it not alright, please, be careful using these results'
    multicorrelation_number = results.condition_number
    if multicorrelation_number <= 20:
        multicorrelation_message = 'Great, there is no multicorrelation!!!'
    else:
        multicorrelation_message = '''Damn, there is multicorrelation. But it is fine, coz some 
                                    scientists believe that it does not really matter'''
    save_boxplot(data, factors.keys())
    boxplot_dirs = []
    for factor in factors.keys():
        boxplot_dirs.append('../static/'+factor+'.png')
    
    return  (info, p_value_norm, distribution, dw_stat, dw_decision, 
            homoscedasticity, homoscedasticity_pv, multicorrelation_number,
            homoscedasticity_decision, multicorrelation_message, 
            list(factors.keys()), boxplot_dirs, anova_factors)
    
    
def get_info_important_factors(important_factors):
    all_res_statistics = []
    for factors in important_factors:
        res = "Income ~ "
        splitted_factors = factors.split('__')
        for factor in splitted_factors:
            res += 'C(' + factor + ')'
        res = res.replace(')C', ')*C')
        
        res_statistics = {}
        data = get_data()
        p_value_norm, distribution = check_normality(data)
        if distribution == 'Not normal':
            data = data[:100]
            data['Income'] = data[['Income']].applymap(lambda x: np.log(x+1))
            q25, q75 = np.percentile(data['Income'], 25), np.percentile(data['Income'], 75)
            iqr = q75 - q25
            cut_off = iqr * 1.5
            lower, upper = q25 - cut_off, q75 + cut_off
            data = data[data['Income'] > lower]
            data = data[data['Income'] < upper] 
        model = ols(res, data)
        results = model.fit()
        results.summary()
        res_statistics['dw_stat'], res_statistics['dw_decision'] = check_autocorrelation(results.resid.values)
        res_statistics['homoscedasticity'], res_statistics['homoscedasticity_pv'] = results.diagn['omni'], results.diagn['omnipv']
        if res_statistics['homoscedasticity_pv'] > 0.05:
            res_statistics['homoscedasticity_decision'] = 'there is no homescedasticity and we may believe observed results'
        else:
            res_statistics['homoscedasticity_decision'] = 'it not alright, please, be careful using these results'
        res_statistics['multicorrelation_number'] = results.condition_number
        if res_statistics['multicorrelation_number'] <= 20:
            res_statistics['multicorrelation_message'] = 'Great, there is no multicorrelation!!!'
        else:
            res_statistics['multicorrelation_message'] = '''Damn, there is multicorrelation. But it is fine, coz some 
                                        scientists believe that it does not really matter'''
        all_res_statistics.append(res_statistics)
    return all_res_statistics
        
        
        
        
        
        
        