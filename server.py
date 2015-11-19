# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager


app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/test1'
db = SQLAlchemy(app)
restless = APIManager(app, flask_sqlalchemy_db=db)


class User(db.Model):

    """
    user
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255), nullable=False)


restless.create_api(
    User, methods=['GET', 'POST', 'DELETE',
                   'PATCH', 'PUT'], results_per_page=100)

db.create_all()

if __name__ == '__main__':
    # session = db.session()
    # session.add(User(id=1, username='Joseph Lee', password='940622'))
    # session.commit()
    app.run(port=20000)
