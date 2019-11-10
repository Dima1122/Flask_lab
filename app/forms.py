from flask_wtf import Form
from wtforms import StringField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, regexp, AnyOf, ValidationError, NumberRange

def my_length_check(form, field):
    if len(field.data) > 5:
        raise ValidationError('Field must be less than 50 characters')

class ObservationForm(Form):
    def if_number(self, form, field):
        try:
            int(field.data)
        except ValueError:
            raise ValidationError('Field must be number')

    ID = IntegerField('ID', validators = [DataRequired()])
    EmploymentField = StringField('EmploymentField', validators = [DataRequired()])
    EmploymentStatus = SelectField('EmploymentStatus', choices=[("Employed for wages",'Employed for wages'),("Self-employed business owner",'Self-employed business owner'),('Self-employed freelancer', 'Self-employed freelancer'), ('Unemployed', 'Unemployed')])
    Gender = SelectField("Gender: ", choices=[("male",'male'),("female",'female'),('bisexual', 'bisexual')])
    LanguageAtHome = StringField('LanguageAtHome', validators = [DataRequired()])
    JobWherePref = StringField('JobWherePref', validators = [DataRequired()])
    SchoolDegree = StringField('SchoolDegree', validators = [DataRequired()])
    Income = FloatField('Income', validators = [DataRequired()])