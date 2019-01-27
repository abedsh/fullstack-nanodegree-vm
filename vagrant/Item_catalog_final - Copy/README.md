# Description

An item catalog web app

# Install
This project requires Python 2.7.12 and sql lite

# Code backend

__init__.py - Define all the essential apis the app will need, (login_manager, db_session, flask app) 
model.py - Defines all sqlalchamy models used for crud operations, in addition to the flask login user class
db_utils.py - Defines generic(for any type of a declared sqlalchamy model) sqlalchamy query operations
views.py - Defines all the routed views of the app
run.py - Defines the runner of the app
client_secrets.json refer to https://developers.google.com/identity/sign-in/web/server-side-flow for steps to create your own client_secrets.json file



# Code frontend

static/js/login_gmail.js Defines callback function to the 
header.html - Defines the header of the view, and login/logout callbacks, include the client id from the generated client_secret.json 
index.html - Defines the home view
item_details - Defines item details view
category_details - Defines category details view


# How to

Compile and run the run.py to start the server on localhost:5000

