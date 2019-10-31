CSRF_ENABLED = True
SECRET_KEY = 'Wanna-hack-my-site?Then-I-will-hack-yours'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DATABASE = 'app.sqlite'
