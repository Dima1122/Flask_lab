from app import app
from flask import render_template, flash, redirect, g
from flask import request, escape
from analysis import analyzer
from app.forms import ObservationForm
import sqlite3

'''def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()'''

@app.route('/')
@app.route('/index', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/analysis', methods=['GET'])
def analysis():
    field1 = escape(request.args.get('field1'))
    field2 = escape(request.args.get('field2'))
    contingency_table = analyzer.get_contingency_table(field1, field2)
    expected_table = analyzer.get_expected_table(field1, field2)
    statistic_name, p_value = analyzer.get_statistic(field1, field2) 
    return render_template('analysis.html', contingency_table = contingency_table, expected_table = expected_table, statistic_name = statistic_name, p_value = p_value)

@app.route('/add_row', methods=['GET'])
def add_row():
    form = ObservationForm()
    return render_template('add_row.html', form=form)

@app.route('/add_row', methods=['POST'])
def insert_row():
    form = ObservationForm()
    '''
    Здесь будет код вставки в БД
    '''
    conn = sqlite3.connect(app.config['DATABASE'])
    g.db = conn
    id = g.db.execute('select max(id) from observation').fetchall()[0][0] + 1
    g.db.execute('insert into observation values (?, ?, ?, ?, ?, ?, ?, ?)',
                 [id, request.form['EmploymentField'], request.form['EmploymentStatus'], request.form['Gender'], request.form['LanguageAtHome'],
                 request.form['JobWherePref'], request.form['SchoolDegree'], request.form['Income']])
    g.db.commit()
    g.db.close()
    flash('Добавлена запись:\nEmploymentField = ' + str(form.EmploymentField.data) + '\nEmploymentStatus = ' + str(form.EmploymentStatus.data) + '\nGender = ' + str(form.Gender.data) +
          '\nLanguageAtHome = ' + str(form.LanguageAtHome.data) + '\nJobWherePref = ' + str(form.JobWherePref.data) + '\nSchoolDegree = ' + str(form.SchoolDegree.data) +
          '\nIncome = ' + str(form.Income.data))
    return redirect('/index')

