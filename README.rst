##########################
ES Python Microservice
##########################

Sample API to search books using FastAPI and ElasticSearch

===================
Running the project
===================

* Build the docker image::

    docker-compose build

* Populate with sample data::

    docker-compose run --rm api poetry run python populate.py data.json

* Run the docker-compose::

    docker-compose up


API will be available at `http://localhost:5000/api/v1/search <http://localhost:5000/api/v1/search>`_

See `API Documentation <http://localhost:5000/docs>`_
