#Import all dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Create engine for flask 
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

#Create a variable for each class
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create a session link
session = Session(engine)

#Define our flask app
app = Flask(__name__)

#Define our flask welcome route
@app.route("/")

#Add all other routing information - this def function is needed after the above command
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#Make another route
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Calculate the date one year ago
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   #Query the date and precipitation for the previous year
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    #Define the key and value for your json output
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    #Create query to get all stations from database
    results = session.query(Station.station).all()
    #Convert results into a list
    stations = list(np.ravel(results))
    #Jsonify the list
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    #Calculate the date one year ago
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #Query the primary station and temperature observed over the past year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    #Unravel results into a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/start")
@app.route("/api/v1.0/temp/start/end")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

    