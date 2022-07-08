from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

# connect to sql db on heroku
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL').replace("://", "ql://", 1)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# set up car model


class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self, name, model, doors):
        self.name = name
        self.model = model
        self.doors = doors

    def __repr__(self):
        return f"<Car {self.name}>"

# this stuff returns json


@app.route('/cars', methods=['POST', 'GET', 'DELETE'])
def handle_cars():
    if request.method == 'POST':
        # if request.is_json:
        data = request.get_json()
        new_car = CarsModel(name=data['name'],
                            model=data['model'], doors=data['doors'])
        db.session.add(new_car)
        db.session.commit()
        return {"message": f"car {new_car.name} has been created successfully."}
        # else:
        #     return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        cars = CarsModel.query.all()
        results = [
            {
                "id": car.id,
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]
        return {"count": len(results), "cars": results}

# crud get by ids


@app.route('/cars/<id>', methods=['GET', 'DELETE', 'PATCH'])
def get_single_car(id):
    if request.method == 'GET':
        car = CarsModel.query.get(id)
        results = {
            "id": car.id,
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        }
        return results

    elif request.method == 'DELETE':
        CarsModel.query.filter_by(id=id).delete()
        db.session.commit()

        return {"message": f"car has been deleted successfully."}

    elif request.method == 'PATCH':
        data = request.get_json()
        db.session.query(CarsModel).filter(
            CarsModel.id == id).update({'model': data['model']})
        db.session.commit()

        return {"message": f"car has  been updated successfully."}

# these routes use templates


@app.route('/', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def members_handler():
    if request.method == 'POST':

        new_car = CarsModel(
            name=request.form['name'], model=request.form['model'], doors=request.form['doors'])
        db.session.add(new_car)
        db.session.commit()

        cars = CarsModel.query.all()
        results = [
            {
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]

        return render_template('index.html', members=results)

    elif request.method == 'GET':
        cars = CarsModel.query.all()
        results = [
            {
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]
        html_to_send = render_template('index.html', members=results)
        return html_to_send

    elif request.method == 'DELETE':
        CarsModel.query.filter_by(id=10).delete()
        db.session.commit()

        return {"message": f"car has been deleted successfully."}

    elif request.method == 'PATCH':
        db.session.query(CarsModel).filter(
            CarsModel.id == 2).update({'model': 'vw'})
        db.session.commit()

        return {"message": f"car has  been updated successfully."}
