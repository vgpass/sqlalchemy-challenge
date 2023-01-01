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
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"<h2><b>Welcome to the Climate App API!</b></h2><br/>"
        f"<h3><b>Vincent Passanisi<br/>"
        f"December 2022 - UCI Data Analytics Bootcamp<br/>"
        f"<br/>"
        f"Here are the Available Routes:</b></h3><br/>"
        f"<b>For a JSON of the precipitation analysis, use this route:</b><br/>"
        f"<br/><font size=5>"
        f"<i>/api/v1.0/precipitation</i><br/>"
        f"<br/></font size=5>"
        f"<b>For a JSON list of stations in the dataset, use this route:</b><br/>"
        f"<br/><font size=5>"
        f"<i>/api/v1.0/stations</i><br/>"
        f"<br/></font size=5>"
        f"<b>For a JSON list of temperature observations for the previous year for the most active station, use this route:</b><br/>"
        f"<br/><font size=5>"
        f"<i>/api/v1.0/tobs</i><br/>"
        f"<br/></font size=5>"
        f"<b>For a JSON list of the minimum temperature, the average temperature, and the maximum temperature,"
        f"for a specified start date for each station,<br/>"
        f"append a start date to the route in the format yyyy-mm-dd</b><br/>"
        f"<br/><font size=5>"
        f"<i>/api/v1.0/<start></i><br/>"
        f"<br/></font size=5>"
        f"<b>For a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified date range,<br/>"
        f"append a start and end date in the format yyyy-mm-dd/yyyy-mm-dd</b><br/>"
        f"<br/><font size=5>"
        f"<i>/api/v1.0/<start>/<end></i><br/>"
        f"<br/></font size=5>"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    """Return the climate app precipitation data as json"""
    # Starting from the most recent data point in the database. 
    current = dt.date(2017, 8, 23)
    
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

# Get a list of stations in the dataset and return a json
@app.route("/api/v1.0/stations")
def stations():

    station_list = session.query(Station.station, Station.name).all()

    session.close()

    station_list_dict = dict(station_list)
    return jsonify(station_list_dict)



# JSON list of temperature observations for the previous year for the most active station
@app.route("/api/v1.0/tobs")
def most_active():

    current = dt.date(2017, 8, 23)
    year_ago = current - dt.timedelta(days=365)

    most_active_station_temp = session.query(Measure.date, Measure.tobs).\
        filter(Measure.station == 'USC00519281').\
        filter(Measure.date >= year_ago).\
        filter(Measure.date <= current).\
        order_by(Measure.date).all()

    session.close()

    active_tobs = dict(most_active_station_temp)
    return jsonify(active_tobs)

# JSON list of the minimum temperature, the average temperature, and the maximum temperature by station starting with a specified date
@app.route("/api/v1.0/<start>")
def start(start=None):
    
    
    temp_start = session.query(func.min(Measure.tobs)\
        , func.max(Measure.tobs)\
        , func.round(func.avg(Measure.tobs),2), Station.name).\
        filter(Measure.station == Station.station).\
        filter(Measure.date >= start).\
        group_by(Measure.station).all()

    session.close()

    start_data = []
    for tmin, tmax, tavg, name in temp_start:
        start_dict = {}
        start_dict['tmin'] = tmin
        start_dict['tmax'] = tmax
        start_dict['tavg'] = tavg
        start_dict['name'] = name
        start_data.append(start_dict)

    return jsonify(start_data)


# JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified date range
@app.route("/api/v1.0/<start>/<end>")
def range(start=None, end=None):
    
    temp_range = session.query(func.min(Measure.tobs)\
        , func.max(Measure.tobs)\
        , func.round(func.avg(Measure.tobs),2), Station.name).\
        filter(Measure.station == Station.station).\
        filter(Measure.date >= start).\
        filter(Measure.date <= end).\
        group_by(Measure.station).all()

    session.close()

    range_data = []
    for tmin, tmax, tavg, name in temp_range:
        range_dict = {}
        range_dict['tmin'] = tmin
        range_dict['tmax'] = tmax
        range_dict['tavg'] = tavg
        range_dict['name'] = name
        range_data.append(range_dict)

    return jsonify(range_data)


if __name__ == '__main__':
    app.run(debug=True)