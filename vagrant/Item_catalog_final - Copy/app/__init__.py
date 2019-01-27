'''
Created on Aug 30, 2018

@author: abedch
'''

from flask import Flask, url_for, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager, login_user

# init essentail lib for flask
app = Flask(__name__)


# init login manager
login_manager = LoginManager()

login_manager.init_app(app)

# init db model utils

Base = declarative_base()

engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)


Base.metadata.bind = engine

Session = sessionmaker()
Session.configure(bind=engine)

db_session = Session()

from app import models, views
