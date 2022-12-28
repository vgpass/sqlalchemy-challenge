from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()


# reflect the tables
Base.prepare(autoload_with=engine)

# View all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measure = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precip():
    """Return the climate app precipitation data as json"""
    # Starting from the most recent data point in the database. 
    session = Session(engine)
    # Calculate the date one year from the last date in data set.

    current = dt.date(2017, 8, 23)
    year_ago = current - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores

    last_year_prcp = session.query(Measure.date, Measure.prcp).\
        filter(Measure.date >= year_ago).\
        filter(Measure.date <= current).\
        order_by(Measure.date).all()

    session.close()
    # Save the query results as a Pandas DataFrame and set the index to the date column

    rain_df = dict(last_year_prcp)
    return jsonify(rain_df)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )