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
from flasgger import Swagger
from sqlalchemy import or_


swagger = Swagger(app)


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
    date_format = "%d %b %y"

    def __init__(self, date_str):
        try:
            self.value = datetime.strptime(date_str, self.date_format).date()
        except ValueError:
            abort(400, {'message': 'Date must be in format %d %b %y. Try something similar to 30 sep 17'})



@app.route("/")
def index():
    return 'Hey Flybits!'


@app.route("/drink", methods=['POST'])
def create():
    """
    Creates a new drink object and adds it to the table of drinks
    Example:
        - name: Coke
        - price: 2.50
        - start_availability_date: 28 feb 17
        - end_availability_date: 28 feb 18
    ---
    parameters:
        - name: name
          in: query
          type: string
          required: true
        - name: price
          in: query
          type: number
          required: true
        - name: start_availability_date
          in: query
          type: string
          required: true
        - name: end_availability_date
          in: query
          type: string
          required: false
    definitions:
        Response:
            type: object
            properties:
                message:
                    type: string
    responses:
        200:
            description: Successfully added the new drink
            schema:
                $ref: '#/definitions/Response'
    """
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
    """
        Deletes drink by id
        Example (delete drink with id 1):
            - DEL /drink/1
        ---
        parameters:
            - name: id
              in: path
              type: integer
              required: true
        definitions:
            Response:
                type: object
                properties:
                    message:
                        type: string
        responses:
            200:
                description: Successfully deleted the drink
                schema:
                    $ref: '#/definitions/Response'
        """
    if not db.session.query(Drink).filter(Drink.id == id).first():
        abort(404, {'message': 'Drink with id {} does not exist'.format(id)})

    db.session.query(Drink).filter(Drink.id == id).delete()
    db.session.commit()
    return json.dumps({'message': 'Successfully deleted drink with id {}'.format(id)}), 200


@app.route("/drink/search", methods=['GET'])
def search():
    """
        Searches for all drinks that match a given search criteria
        Example 1 (no search criteria - returns all drinks):
        Example 2 (search for drinks whose name is like Coke):
            - name: Coke
        Example 3 (search for drinks available on 1 feb 17):
            - available_on_day: 1 feb 17
        Example 4 (search for drinks available on 1 feb 17 whose name is like Coke):
            - name: Coke
            - available_on_day: 1 feb 17
        ---
        parameters:
            - name: name
              in: query
              type: string
              required: false
            - name: available_on_day
              in: query
              type: string
              required: false
        definitions:
            Drink:
                type: object
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                    price:
                        type: number
                    start_availability_date:
                        type: string
                    end_availability_date:
                        type: string
            Drinks:
                type: array
                items:
                    $ref: '#definitions/Drink'
        responses:
            200:
                description: Successfully added the new drink
                schema:
                    $ref: '#/definitions/Drinks'
                examples:
                    [{
                        "price": 10.0,
                        "end_availability_date": null,
                        "id": 2,
                        "start_availability_date": "2016-04-30",
                        "name": "apple juice"
                     }]
    """
    # TODO: Add price filter
    name = str(request.args.get('name')) if request.args.get('name') else None
    available_on_day = AvailabilityDate(str(request.args.get('available_on_day'))) \
        if request.args.get('available_on_day') else None

    query = db.session.query(Drink)

    if name:
        query = query.filter(Drink.name.like('%{}%'.format(name)))

    if available_on_day:
        query = query.filter(available_on_day.value >= Drink.start_availability_date)\
            .filter(or_(Drink.end_availability_date == None, available_on_day.value <= Drink.end_availability_date))

    results = query.all()

    return json.dumps([{
        "id": result.id,
        "name": result.name,
        "price": result.price,
        "start_availability_date": str(result.start_availability_date),
        "end_availability_date": str(result.end_availability_date) if result.end_availability_date else None,
    } for result in results]), 200
