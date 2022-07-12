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


class URLModel(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String())
    short_url = db.Column(db.String())

    def __init__(self, url, short_url):
        self.url = url
        self.short_url = short_url

    def __repr__(self):
        return f"<Url {self.name}>"

# this stuff returns json


@app.route('/cars', methods=['POST', 'GET', 'DELETE'])
def handle_cars():
    if request.method == 'POST':
        # if request.is_json:
        data = request.get_json()
        short_url = 'do something here to shorten the url'
        new_url = URLModel(url=data['url'], short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return {"message": f"car {new_car.name} has been created successfully."}
        # this is where we then redirect to the page
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


@app.route('/', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def members_handler():
    # shortern url here on post + store in db with original url
    if request.method == 'POST':
        # check to see if we have got the url in db if so reroute
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
