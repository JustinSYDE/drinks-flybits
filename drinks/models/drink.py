from drinks import db
from datetime import date


class Drink(db.Model):
    __tablename__ = 'drink'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    start_availability_date = db.Column(db.Date, nullable=False, default=date.today())
    end_availability_date = db.Column(db.Date)

    def __init__(self, name, price, start_availability_date, end_availability_date=None):
        self.name = name
        self.price = price
        self.start_availability_date = start_availability_date
        self.end_availability_date = end_availability_date
