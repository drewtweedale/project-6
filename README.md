# UOCIS322 - Project 6 #
Brevet time calculator with MongoDB, and a RESTful API!

Read about MongoEngine and Flask-RESTful before you start: [http://docs.mongoengine.org/](http://docs.mongoengine.org/), [https://flask-restful.readthedocs.io/en/latest/](https://flask-restful.readthedocs.io/en/latest/).

## Author
Ali Hassani, Drew Tweedale. Contact: dtweedal@uoregon.edu


## Project

* This project is an implementation of a RESTful API in `api/`:
	* The data schema uses MongoEngine for Checkpoints and Brevets:
		* `Checkpoint`:
			* `distance`: float, required, (checkpoint distance in kilometers), 
			* `location`: string, optional, (checkpoint location name), 
			* `open_time`: datetime, required, (checkpoint opening time), 
			* `close_time`: datetime, required, (checkpoint closing time).
		* `Brevet`:
			* `length`: float, required, (brevet distance in kilometers),
			* `start_time`: datetime, required, (brevet start time),
			* `checkpoints`: list of `Checkpoint`s, required, (checkpoints).
	* Using the schema, the RESTFul API uses the resource `/brevets/`:
		* GET `http://API:PORT/api/brevets` displays all brevets stored in the database.
		* GET `http://API:PORT/api/brevet/ID` displays brevet with id `ID`.
		* POST `http://API:PORT/api/brevets` inserts brevet object in request into the database.
		* DELETE `http://API:PORT/api/brevet/ID` deletes brevet with id `ID`.
		* PUT `http://API:PORT/api/brevet/ID` updates brevet with id `ID` with object in request.
