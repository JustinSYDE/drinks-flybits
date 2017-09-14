from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import os

url = os.getenv('DATABASE_URL')
engine = create_engine('sqlite:///' + os.getenv('DATABASE_URL'))
session = Session(engine)

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "hello"

if __name__ == "__main__":
    app.run()