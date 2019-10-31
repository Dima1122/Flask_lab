from app import db

class Observation(db.Model):
    ID = db.Column(db.Integer())
    EmploymentField = db.Column(db.String(120))
    EmploymentStatus = db.Column(db.String(120))
    Gender = db.Column(db.String(120))
    LanguageAtHome = db.Column(db.String(120))
    JobWherePref = db.Column(db.String(120))
    SchoolDegree = db.Column(db.String(120))
    Income = db.Column(db.Float)
