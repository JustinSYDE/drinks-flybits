from config import Config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

app = create_app(Config)
db = SQLAlchemy(app)

from drinks import controllers