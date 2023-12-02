"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import os
import flask
import requests
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import logging

###
# Globals
###
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)

##################################################
################### API Callers ################## 
##################################################

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"

###
# Below are the MongoDB functions that were originally located in the database.
###

def get_brev():
    """
    Obtains the newest document in the "lists" collection in database "brevetsdb".

    Returns  (string) and items (list of dictionaries) as a tuple.
    """
    
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    lists = requests.get(f"{API_URL}brevets").json()

    # lists should be a list of dictionaries.
    # we just need the last one:
    brevet = lists[-1]
    return brevet["length"], brevet["start_time"], brevet["checkpoints"]

def get_brev_unique(id):
    brev = requests.get(f"{API_URL}/brevet/{id}").json()
    return brev

def get_all():
    brevs = requests.get(f"{API_URL}/brevets").json()
    return brevs

def insert_brev(brev_dist, start_time, items):
    """
    Inserts a new brev into the database "brevetsdb", under the collection "lists".
    
    Inputs a brev_dist, start time and the required controle distances, 
    and open and close times (list of dictionaries)

    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    _id = requests.post(f"{API_URL}brevets", json={"length": brev_dist, "start_time": start_time, "checkpoints": items}).json()
    return _id


def delete(id):
    requests.delete(f"{API_URL}/brevet/{id}")
    return

def update(id, brev_dist, start_time, items):
    requests.put(f"{API_URL}/brevets/{id}", json={"length": brev_dist, "start_time": start_time, "checkpoints": items}).json()
    return


###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    start_time = request.args.get('start_time')
    brevet_dist = request.args.get('brev_dist', type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    open_time = acp_times.open_time(km, brevet_dist, arrow.get(start_time)).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist, arrow.get(start_time)).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/submit", methods=["POST"])
def insert():
    """
    /submit : inserts a controle distance (and the respective times) into the database.

    Accepts POST requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        brev_dist = input_json["brev_dist"] # Should be a string
        start_time = input_json["start_time"] # Should be a string
        items = input_json["items"] # Should be a list of dictionaries
        if len(items) == 0:
            return flask.jsonify(
                message ="No controle distances were entered.",
                status = 0
            )
        brev_id = insert_brev(brev_dist, start_time, items)

        return flask.jsonify(result={},
                        message="Inserted!", 
                        status=1, # This is defined by you. You just read this value in your javascript.
                        mongo_id=brev_id)
    except Exception:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')

@app.route("/display")
def fetch():
    """
    /display : fetches the newest to-do list from the database.

    Accepts GET requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        brev_dist, start_time, items = get_brev()
        return flask.jsonify(
                result={"brevet_dist_km": brev_dist, "begin_date": start_time, "items": items}, 
                status=1,
                message="Successfully fetched a brevet")
    except:
        return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't fetch the brevet!")

@app.route("/api/brevet/<id>", methods=["GET", "PUT", "DELETE"])
def particular_brevet(id):
    if request.method == "GET":
        try:
            brev = get_brev_unique(id)
            id = brev["id"]
            length = brev["length"]
            start_time = brev["start_time"]
            checkpoints = brev["checkpoints"]
            final={"id": id, "brevet_dist_km": length, "begin_date": start_time, 
            "items": checkpoints}
            return flask.jsonify(final)
        except:
            return flask.jsonify(
                    result={}, 
                    status=0,
                    message="Something went wrong, couldn't fetch any brevet data!")
        
    elif request.method == "DELETE":
        try:
            delete(id)
            return flask.jsonify(
                result={},
                status=1,
                message="Deleted the brevet!")
        except:
            return flask.jsonify(
                    result={}, 
                    status=0,
                    message="Error in deleting the brevet!")
        
    elif request.method == "PUT":
        try:
            input_json = request.json
            # if successful, input_json is automatically parsed into a python dictionary
            
            brev_dist = input_json["brevet_dist_km"] # Should be a string
            start_time = input_json["begin_date"] # Should be a string
            items = input_json["items"] # Should be a list of dictionaries
            update(id, brev_dist, start_time, items)
            return flask.jsonify(
                result={},
                status=1,
                message="Updated the brevet!")
        except:
            return flask.jsonify(
                    result={}, 
                    status=0,
                    message="Error in updating brevet!")
    
@app.route("/api/brevets", methods=["POST", "GET"])
def all_brev():
    """
    API endpoint for GET and POST requests:
        GET: Displays all brevets in the collection.
        POST: Insert a brevet into the collection.
    """
    if request.method == "GET": 
        try:
            final = []
            for brevet in get_all():
                id = brevet["id"]
                length = brevet["length"]
                start_time = brevet["start_time"]
                checkpoints = brevet["checkpoints"]
                result={"id": id, "brevet_dist_km": length, "begin_date": start_time, 
                        "items": checkpoints}
                final.append(result)
            return flask.jsonify(final)
        except:
            return flask.jsonify(
                    result={}, 
                    status=0,
                    message="Something went wrong, couldn't fetch any brevet data!")
        
    if request.method == "POST":
        try:
            # Read the entire request body as a JSON
            # This will fail if the request body is NOT a JSON.
            input_json = request.json
            # if successful, input_json is automatically parsed into a python dictionary!
        
            # Because input_json is a dictionary, we can do this:
            brev_dist = input_json["brev_dist"] # Should be a string
            start_time = input_json["start_time"] # Should be a string
            items = input_json["items"] # Should be a list of dictionaries
            if len(items) == 0:
                return flask.jsonify(
                    message ="No controle distances were entered.",
                    status = 0
                )
            brev_id = insert_brev(brev_dist, start_time, items)
            return flask.jsonify(result={},
                            message="Inserted!", 
                            status=1, # This is defined by you. You just read this value in your javascript.
                            mongo_id=brev_id)
        except Exception:
            # The reason for the try and except is to ensure Flask responds with a JSON.
            # If Flask catches your error, it means you didn't catch it yourself,
            # And Flask, by default, returns the error in an HTML.
            # We want /insert to respond with a JSON no matter what!
            return flask.jsonify(result={},
                            message="Oh no! Server error!", 
                            status=0, 
                            mongo_id='None')
    
#############

if __name__ == "__main__":
    app.run(port=port_num, host="0.0.0.0")
