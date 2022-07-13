import string
import random
from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug import exceptions
import os

# connect to sql db on heroku
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL').replace("://", "ql://", 1)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))
    return result_str


class URLModel(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String())
    short_url = db.Column(db.String())

    def __init__(self, url, short_url):
        self.url = url
        self.short_url = short_url

    def __repr__(self):
        return f"<Url {self.url}>"


@app.route('/', methods=['GET', 'POST'])
def members_handler():
    # shortern url here on post + store in db with original url
    if request.method == 'POST':
        data = request.form['url']
        print(data)
        # check to see if we have got the url in db if so, reroute to the url
        # get all long urls from db and check to see if form data matches anything in db
        # this below might work?? not sure what it returns if no query is found
        # if URLModel.query.filter_by(url=data['url']):
        #     # if this is true then we get the short url that links to the long one and redirect
        #     pass
        # else:
        # if not do the below
        # this gets the form input
        short_url = get_random_string(6)
        # do something here to shorten url
        # below adds long url and short url to the model
        new_url = URLModel(url=data, short_url=short_url)
        # below adds new_url to the db
        db.session.add(new_url)
        # below saves the data
        db.session.commit()
        return redirect(f'https://flaskshorturl.herokuapp.com/{short_url}')
        # return {'WORKING '}

# this is the home route should just render the for
    elif request.method == 'GET':
        html_to_send = render_template('index.html')
        return html_to_send


@app.route('/<shorturl>', methods=['GET'])
def redirect_shorturl(shorturl):
    # this takes the url from the user
    url = URLModel.query.filter_by(short_url=shorturl).first()
    print(url)
    long_url = url['url']
    print(long_url)
    # this is then where we need to grab the long url from the db
    # redirect using url.url or something?
    # then we redirect the page
    return redirect(long_url)


@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return {'message': f'Oops! {err}'}, 404


@app.errorhandler(exceptions.BadRequest)
def handle_400(err):
    return {'message': f'Oops! {err}'}, 400


@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return {'message': f"It's not you, it's us"}, 500


if __name__ == "__main__":
    app.run(debug=True)
