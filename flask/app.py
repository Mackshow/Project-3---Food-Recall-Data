# import necessary libraries
import numpy as np
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, render_template, request, jsonify, redirect


##########################################
# Database Setup
##########################################

engine = create_engine("sqlite:///db/foodReactions0.sqlite", echo=False)

# Base definition, reflect an existing DB into a new model
base = automap_base()

# Reflect the DB Tables
base.prepare(engine, reflect=True)

#Save references to each table
reactions= base.classes.reactions
prooducts= base.classes.products

#Create our session from Python to the DB
session = Session(engine)


################################################
# Flask Setup
##################################################

app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)
