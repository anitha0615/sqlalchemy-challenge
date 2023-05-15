# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement


# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available routes"""
    
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipiation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )



@app.route("/api/v1.0/precipiation")
def precipitation():
    """Add query reults into a dictionary, then jsonify it."""

    last_12_months = session.query(Measurement).filter(Measurement.date >="2016-08-23")
    date = []
    precipitation = []
    for twelve_mon in last_12_months:
        date.append(twelve_mon.date)
        precipitation.append(twelve_mon.prcp)
    dp_dict = dict(zip(date, precipitation))
    return jsonify(dp_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations in json format."""
    
    station_count = session.query(Station.station).all()
    stations_list = []
    for result in station_count:
        stations_list.append(result[0])
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return dates and temperature observations for most active station in json format."""

    temp_active = []
    temp_analysis = session.query(Measurement).filter(Measurement.station >="USC00519281")
    for i in temp_analysis:
        temp_active.append(i.tobs)
    return jsonify(temp_active)   


@app.route("/api/v1.0/<start>", methods = ['GET'])
def start(start):
    """Return JSON list of min, avg, and max temperature from a specified start date."""

    min_temperature = session.query(func.min(Measurement.tobs))\
    .filter(Measurement.date >= start).first()
    max_temperature = session.query(func.max(Measurement.tobs))\
    .filter(Measurement.date >= start).first()
    avg_temperature = session.query(func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start).first()

    results_temperature = {"min": min_temperature,"max":max_temperature,"avg":avg_temperature}

    return jsonify(results_temperature)


@app.route("/api/v1.0/<start>/<end>", methods = ['GET'])
def start_end(start,end):
    """Return JSON list of min, avg, and max temperature for a specified range of dates."""

    min_temperature = session.query(func.min(Measurement.tobs))\
    .filter((Measurement.date.between(start,end))).first()
    max_temperature = session.query(func.max(Measurement.tobs))\
    .filter((Measurement.date.between(start,end))).first()
    avg_temperature = session.query(func.avg(Measurement.tobs))\
    .filter((Measurement.date.between(start,end))).first()

    results_range_temp = {"min": min_temperature,"max": max_temperature, "avg":avg_temperature}

    return jsonify(results_range_temp)


if __name__ == '__main__':
    app.run(debug=True)