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
from sqlalchemy import or_


class Price:
    """
    valid price: 2, 2.22, 2.5
    """
    def __init__(self, value):
        try:
            self.value = "{:.2f}".format(value)
        except ValueError:
            abort(400, {'message': 'Price must be an integer or a float x or x.xx'})


class AvailabilityDate:
    """
    valid date: 30 nov 17
    """
    datetime_format = "%d %b %y"

    def __init__(self, date_str):
        try:
            self.value = datetime.strptime(date_str, self.datetime_format)
        except ValueError:
            abort(400, {'message': 'Date must be in format %d %b %y. Try something similar to 30 sept 17'})



@app.route("/")
def index():
    return 'Hey Flybits!'


@app.route("/drink", methods=['POST'])
def create():
    name = str(request.args.get('name'))
    price = Price(float(request.args.get('price')))
    start_date_str = str(request.args.get('start_availability_date'))
    end_date_str = str(request.args.get('end_availability_date')) \
        if request.args.get('end_availability_date') else None
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
    return json.dumps({'message': 'Successfully added {} as new drink'.format(name)}), 200


@app.route("/drink/<id>", methods=['DELETE'])
def delete_by_id(id):
    if not db.session.query(Drink).filter(Drink.id == id).first():
        abort(404, {'message': 'Drink with id {} does not exist'.format(id)})

    db.session.query(Drink).filter(Drink.id == id).delete()
    db.session.commit()
    return json.dumps({'message': 'Successfully deleted drink with id {}'.format(id)}), 200


@app.route("/drink/search", methods=['GET'])
def search():
    # TODO: Add price filter
    name = str(request.args.get('name')) if request.args.get('name') else None
    available_on_day_str = str(request.args.get('available_on_day')) \
        if request.args.get('available_on_day') \
        else datetime.today().strftime('%d %b %y')
    available_on_day = AvailabilityDate(available_on_day_str)

    query = db.session.query(Drink)\
        .filter(available_on_day.value >= Drink.start_availability_date)\
        .filter(or_(Drink.end_availability_date == None, available_on_day.value <= Drink.end_availability_date))\

    if name:
        query = query.filter(Drink.name.like('%{}%'.format(name)))

    results = query.all()

    return json.dumps([{
        "id": result.id,
        "name": result.name,
        "price": result.price,
        "start_availability_date": str(result.start_availability_date),
        "end_availability_date": str(result.end_availability_date) if result.end_availability_date else None,
    } for result in results]), 200
