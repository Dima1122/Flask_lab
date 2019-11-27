from app import app
from flask import render_template, flash, redirect, g
from flask import request, escape
from analysis import analyzer, analyzer_2, wine_analyzer
from app.forms import ObservationForm
import sqlite3

WINE_COLS = ['FixedAcidity','VolatileAcidity','CitricAcid','ResidualSugar','Chlorides','FreeSulfurDioxide','TotalSulfurDioxide','Density',
             'PH','Sulphates','Alcohol']

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
    g.db.execute('insert into observation values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 [id, request.form['CityPopulation'], request.form['EmploymentField'], request.form['EmploymentStatus'], request.form['Gender'], request.form['HasDebt'],
                  request.form['LanguageAtHome'], request.form['JobPref'], request.form['JobWherePref'], request.form['MaritalStatus'],
                  request.form['SchoolDegree'], request.form['Income']])
    g.db.commit()
    g.db.close()
    flash('Добавлена запись:\nCityPopulation = ' + str(form.CityPopulation.data) + '\nEmploymentField = ' + str(form.EmploymentField.data) + '\nEmploymentStatus = ' + str(form.EmploymentStatus.data) + '\nGender = ' + str(form.Gender.data) +
          '\nHasDebt = ' + str(form.HasDebt.data) + '\nLanguageAtHome = ' + str(form.LanguageAtHome.data) + '\nJobPref = ' + str(form.JobPref.data) +
          '\nJobWherePref = ' + str(form.JobWherePref.data) + '\nMaritalStatus = ' + str(form.MaritalStatus.data) + '\nSchoolDegree = ' + str(form.SchoolDegree.data) +
          '\nIncome = ' + str(form.Income.data))
    return redirect('/index')


@app.route('/factors', methods=['GET'])
def choose_factors():
    return render_template('factors.html')

@app.route('/factors', methods=['POST'])
def analysis_income():
    if len(request.form) == 0:
        return render_template('factors.html')
    res = 'Income ~ '
    for param in request.form.keys():
        res += 'C(' + param + ')'
    res = res.replace(')C', ')*C')
    (info, p_value_norm, distribution, dw_stat, dw_decision, homoscedasticity, 
     homoscedasticity_pv, multicorrelation_number, homoscedasticity_decision, 
     multicorrelation_message, factors, boxplot_dirs, anova_factors) = analyzer_2.anova_analysis(res)
    all_stat_important_f = analyzer_2.get_info_important_factors(factors)
    
    return render_template('income.html', info = info, p_value_norm =p_value_norm, distribution=distribution,
                           dw_stat = dw_stat, dw_decision = dw_decision, homoscedasticity = homoscedasticity,
                           homoscedasticity_pv = homoscedasticity_pv, homoscedasticity_decision = homoscedasticity_decision,
                           multicorrelation_number = multicorrelation_number, multicorrelation_message = multicorrelation_message,
                           factors = factors, boxplot_dirs = boxplot_dirs, anova_factors = anova_factors, all_stat_important_f = all_stat_important_f)

@app.route('/ellipsis', methods=['GET'])
def choose_pair():
    '''
    выбираем пару для отрисовки
    '''
    return render_template('choose_pair.html', cols=WINE_COLS)

@app.route('/ellipsis', methods=['POST'])
def predictive_ellipsis():
    if len(request.form) != 2: #отрабатываем случай, когда выбрано не 2 переменных
        return render_template('choose_pair.html', cols=WINE_COLS)
    '''
    Здесь будут рассчитываться нужные данные
    Данные лежат в бд в таблице WINE
    '''
    fields = []
    for field in request.form.keys():
        fields.append(field)
    field1 = fields[0]
    field2 = fields[1]
    data = wine_analyzer.get_coordinates(field1, field2)
    return render_template('ellipsis.html', coordinates=data)

@app.route('/wine_pca', methods=['GET'])
def wine_pca():
    data = wine_analyzer.calculate_pca(cols=WINE_COLS)
    return render_template('wine_pca.html', PCA=data)