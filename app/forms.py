from flask_wtf import Form
from wtforms import StringField, FloatField, IntegerField
from wtforms.validators import DataRequired, regexp

class ObservationForm(Form):
    ID = IntegerField('ID', validators = [DataRequired()])
    EmploymentField = StringField('EmploymentField', validators = [DataRequired()])
    EmploymentStatus = StringField('EmploymentStatus', validators = [DataRequired()])
    Gender = StringField('Gender', validators = [DataRequired()])
    LanguageAtHome = StringField('LanguageAtHome', validators = [DataRequired()])
    JobWherePref = StringField('JobWherePref', validators = [DataRequired()])
    SchoolDegree = StringField('SchoolDegree', validators = [DataRequired()])
    Income = FloatField('Income', validators = [DataRequired()])