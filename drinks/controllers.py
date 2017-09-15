import json

from datetime import datetime
from drinks import (
    app,
    db
)
from drinks.models.drink import Drink
from flask import (
    abort,
    request
)


@app.route("/drink/<id>")
def find(id):
    drink = db.session.query(Drink).filter(Drink.id == id).first()
    return drink.name


class Price:
    def __init__(self, value):
        try:
            self.value = "{:.2f}".format(value)
        except ValueError:
            abort(400)


class AvailabilityDate:
    # e.g. 30 nov 17
    datetime_format = "%d %b %y"

    def __init__(self, date_str):
        try:
            self.value = datetime.strptime(date_str, self.datetime_format)
        except ValueError:
            abort(400)


@app.route("/drink", methods=['POST'])
def create():
    name = str(request.args.get('name'))
    price = Price(float(request.args.get('price')))
    start_date_str = str(request.args.get('start_availability_date'))
    end_date_str = str(request.args.get('end_availability_date')) if request.args.get('end_availability_date') else None
    start_availability_date = AvailabilityDate(start_date_str)
    end_availability_date = AvailabilityDate(end_date_str) if end_date_str else None

    drink = Drink(
        name,
        price.value,
        start_availability_date.value,
        end_availability_date.value if end_availability_date else None
    )

    db.session.add(drink)
    db.session.commit()
    return 'success'


@app.route("/drink/search", methods=['GET'])
def search():
    name = str(request.args.get('name'))
    available_on_day_str = str(request.args.get('available_on_day'))
    available_on_day = AvailabilityDate(available_on_day_str)

    results = db.session.query(Drink)\
        .filter(available_on_day.value >= Drink.start_availability_date)\
        .filter(Drink.name.like('%{}%'.format(name))).all()
    return json.dumps([{
        "name": result.__dict__.get('name'),
        "price": result.__dict__.get('price'),
        "start_availability_date": str(result.__dict__.get('start_availability_date')),
        "end_availability_date": str(result.__dict__.get('end_availability_date')) if result.__dict__.get('end_availability_date') else None,
    } for result in results])
