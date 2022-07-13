import string
import random
from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug import exceptions
import os
import html

# connect to sql db on heroku
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL').replace("://", "ql://", 1)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# generates a random string of letters


def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))
    return result_str

# define class


class URLModel(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String())
    short_url = db.Column(db.String(), unique=True)

    def __init__(self, url, short_url):
        self.url = url
        self.short_url = short_url

    def __repr__(self):
        return f"<Url {self.url}>"


@app.route('/', methods=['GET', 'POST'])
def members_handler():
    if request.method == 'POST':
        # get data from form
        data = request.form['url']
        if not data:
            return render_template('link.html', text='Input a URL')
        else:
            # check to see if the url has been used before
            if URLModel.query.filter_by(url=data).first() is not None:
                main = URLModel.query.filter_by(url=data).first()
                # return link already stored in db
                return render_template('link.html', link=f'https://flaskshorturl.herokuapp.com/{main.short_url}')
            else:
                # generate random string of characters
                short_url = get_random_string(10)
                # create new url obg
                new_url = URLModel(url=data, short_url=short_url)
                # add url to db
                db.session.add(new_url)
                db.session.commit()
                # render link on page
                return render_template('index.html', link=f'https://flaskshorturl.herokuapp.com/{short_url}')
    elif request.method == 'GET':
        html_to_send = render_template('index.html')
        return html_to_send


@app.route('/<shorturl>', methods=['GET'])
def redirect_shorturl(shorturl):
    # get long url stored in db by taking in user input
    url = URLModel.query.filter_by(short_url=shorturl).first()
    # redirect user to that url
    return redirect(url.url)


# handle 404
@app.errorhandler(exceptions.NotFound)
def page_not_found(e):
    path = request.path
    return render_template('errors/404.html', path=path), 404

# handle 405


@app.errorhandler(exceptions.BadRequest)
def page_not_found(e):
    path = request.path
    return render_template('errors/405.html', path=path), 405


# handle 500
@app.errorhandler(exceptions.InternalServerError)
def page_not_found(e):
    path = request.path
    return render_template('errors/500.html', path=path), 500


if __name__ == "__main__":
    app.run(debug=True)
