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


@app.route('/', methods=['GET', 'POST'])
def members_handler():
    # shortern url here on post + store in db with original url
    if request.method == 'POST':
        data = request.get_json()
        # check to see if we have got the url in db if so, reroute to the url
        # get all long urls from db and check to see if form data matches anything in db
        # if form data matches -> redirect user to the shorten url
        # if not do the below
        short_url = data['url']
        # do something here to shorten url
        # below adds long url and short url to the model
        new_url = URLModel(url=data['url'], short_url=short_url)
        # below adds new_url to the db
        db.session.add(new_url)
        # below saves the data
        db.session.commit()
        return 'redirect to the short url here'
        # return render_template('index.html')

# this is the home route should just render the for
    elif request.method == 'GET':
        html_to_send = render_template('index.html')
        return html_to_send
