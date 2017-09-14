from config import Config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import date

import os


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
session = Session(engine)
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class Drink(db.Model):
    __tablename__ = 'drink'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    start_availability_date = db.Column(db.DateTime, nullable=False, default=date.today())
    end_availability_date = db.Column(db.DateTime)

    def __init__(self, name, price, start_availability_date, end_availability_date=None):
        self.name = name
        self.price = price
        self.start_availability_date = start_availability_date
        self.end_availability_date = end_availability_date

@app.route("/drink/<id>")
def find(id):
    drink = db.session.query(Drink).filter(Drink.id == id).first()
    return drink.name

@app.route("/write")
def write():
    drink = Drink(
        'Nestea',
        2.50,
        date.today()
    )
    db.session.add(drink)
    db.session.commit()

if __name__ == "__main__":
    app.run()