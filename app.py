# app.py
import os

from flask import Flask
from peewee import SqliteDatabase

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(APP_ROOT, 'database.db')
POKEMON_NAME_LIST = os.path.join(APP_ROOT, "static", "pokemon_names.data")
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "SECRET KEY"
db = SqliteDatabase(app.config['DATABASE'], threadlocals=True)
