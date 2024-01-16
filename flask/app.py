# import necessary libraries
import numpy as np
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, render_template, request, jsonify, redirect

# create instance of Flask app
app = Flask(__name__)

# setup database
engine = create_engine("sqlite:///db/foodReactions.sqlite", echo=False)


Base = automap_base()
Base.prepare(engine, reflect=True)

session = Session(engine)


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        return f'Thank you, {name}! You are {age} years old.'

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    return f'Hello, {name}!'


if __name__ == '__main__':
    app.run(debug=True)
