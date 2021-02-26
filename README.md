# NOM_backend
API and computational layer

## Install for development:
1. install docker and python+pip
2. create and activate a python venv if you so choose (outside of the repository)
    1. 'python3 -m venv \<name of env>'
    2. '. \<name of env>/bin/activate'
3. in the project root, install dependencies using 'pip install -e .'
4. type 'startserver' to start the db container and flask app 



## Debugging with breakpoints (vscode):
1. export FLASK_APP=server (this is the 'name' value in setup.py)
2. use VSCode's 'run and debug' and select the 'Flask' debug cofig
3. path to the application should just be 'app.py'