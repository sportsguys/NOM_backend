# NOM_backend
API and computational layer

## Install for development:
1. install docker and python+pip
2. create and activate a python venv if you so choose (outside of the repository)
    1. 'python3 -m venv \<name of env>'
    2. '. \<name of env>/bin/activate'
3. in the project root, install dependencies using 'pip install -e .'
4. start the database container with docker-compose and create a database called 'football'

- To debug the flask server with breakpoints, export FLASK_APP=server (this is the 'name' value in setup.py) and set application path to app.py