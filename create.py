import os

from flask import Flask, render_template, request
from models import *

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

database_url = config['POSTGRES']['DATABASE_URL']

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
