# Import the dependencies.

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"        
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).\
                filter(measurement.date <= '2017-08-23').\
                filter(measurement.date >= '2016-08-23').\
                all()
    
    session.close()

    last_precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        last_precipitation.append(prcp_dict)

    return jsonify (last_precipitation)
    
@app.route("/api/v1.0/station")
def Station():
    
    session = Session(engine)

    results = session.query(station.name).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    results = session.query(measurement.date, measurement.tobs, measurement.station).\
        filter(measurement.date >= '2016-08-23').\
        filter(measurement.station == 'USC00519281'). all()

    session.close()

    USC00519281_tobs = list(np.ravel(results))

    return jsonify(USC00519281_tobs)    


@app.route("/api/v1.0/<start>")
def start(start=None):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start).all()
    
    session.close()

    start_date = []
    for min_temp, avg_temp, max_temp in results:
        start_date_dict = {}
        start_date_dict["min_temp"] = min_temp
        start_date_dict["avg_temp"] = avg_temp
        start_date_dict["max_temp"] = max_temp
        start_date.append(start_date_dict)

    return jsonify(start_date)


@app.route("/api/v1.0/<start>/<end>")
def start_to_end(start=None,end=None):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date <= end).\
                filter(measurement.date >= start).all()
    
    session.close()

    start_to_close = []
    for min_temp, avg_temp, max_temp in results:
        start_to_close_dict = {}
        start_to_close_dict["min_temp"] = min_temp
        start_to_close_dict["avg_temp"] = avg_temp
        start_to_close_dict["max_temp"] = max_temp
        start_to_close.append(start_to_close_dict) 

    return jsonify(start_to_close)

    

if __name__ == "__main__":
    app.run(debug=True)





