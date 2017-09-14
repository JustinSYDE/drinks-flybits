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
    jsonify,
    request
)


@app.route("/drink/<id>")
def find(id):
    drink = db.session.query(Drink).filter(Drink.id == id).first()
    return drink.name

@app.route("/drink/search", methods=['GET'])
def search():
    pass

@app.route("/drink", methods=['POST'])
def create():
    # e.g. 30 nov 17
    datetime_format = "%d %b %y"
    start_date_input = str(request.args.get('start_availability_date'))
    end_date_input = str(request.args.get('end_availability_date')) if request.args.get('end_availability_date') else None
    start_availability_date = datetime.strptime(start_date_input, datetime_format)
    end_availability_date = datetime.strptime(end_date_input, datetime_format) if end_date_input else None

    drink = Drink(
        str(request.args.get('name')),
        float(request.args.get('price')),
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
