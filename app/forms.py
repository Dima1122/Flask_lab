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

    ID = IntegerField('ID', validators = [DataRequired()]) #нужно ли это здесь?
    CityPopulation = SelectField('EmploymentStatus', choices=[("less than 100,000",'less than 100,000'),("between 100,000 and 1 million",'between 100,000 and 1 million'),('more than 1 million', 'more than 1 million')])
    EmploymentField = StringField('EmploymentField', validators = [DataRequired()])
    EmploymentStatus = SelectField('EmploymentStatus', choices=[("Employed for wages",'Employed for wages'),("Self-employed business owner",'Self-employed business owner'),('Self-employed freelancer', 'Self-employed freelancer'), ('Unemployed', 'Unemployed')])
    HasDebt = SelectField('HasDebt', choices=[("yes",'yes'),("no",'no')])
    Gender = SelectField("Gender: ", choices=[("male",'male'),("female",'female'),('bisexual', 'bisexual')])
    LanguageAtHome = StringField('LanguageAtHome', validators = [DataRequired()])
    JobPref = StringField('JobPref', validators = [DataRequired()])
    JobWherePref = StringField('JobWherePref', validators = [DataRequired()])
    MaritalStatus = SelectField('MaritalStatus', choices=[("single, never married",'single, never married'),("divorced",'divorced'),('separated', 'separated'),('married or domestic partnership','married or domestic partnership')])
    SchoolDegree = StringField('SchoolDegree', validators = [DataRequired()])
    Income = FloatField('Income', validators = [DataRequired()])