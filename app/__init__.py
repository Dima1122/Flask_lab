from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
#data = pd.read_csv('./app/data/data.csv')