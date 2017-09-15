from datetime import (
    date,
    datetime
)
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


@app.route("/drink/search", methods=['GET'])
def search():
    pass


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
        start_availability_date,
        end_availability_date
    )

    db.session.add(drink)
    db.session.commit()
    return 'success'


@app.route("/write")
def write():
    drink = Drink(
        'Nestea',
        2.50,
        date.today()
    )
    db.session.add(drink)
    db.session.commit()
