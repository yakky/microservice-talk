.. _usage:

#####
Usage
#####

API is available at `http://localhost:5000/api/v1/search <http://localhost:5000/api/v1/search>`_

See `documentation <http://localhost:5000/docs>`_


Development mode
################

Run the project in development mode::

    docker-compose up

Production mode
################

Run the project in production mode::

    docker-compose -f docker-compose-production.yml up

Populate with sample data
#########################

You can populate Elasticsearch server with sample data by running the ``populate.py`` command::

    docker-compose run --rm api poetry run python populate.py data.json

``data.json`` is a json file which must be copied to ``tests/data`` directory. Check the provided file for the data schema.
