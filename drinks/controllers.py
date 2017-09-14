from drinks import (
    app,
    db
)
from drinks.models.drink import Drink
from datetime import date


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
