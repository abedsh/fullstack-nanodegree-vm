'''
Created on Aug 30, 2018

@author: abedch
'''
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import string
import random
import json
from dbutils import *
from app import app, login_manager
from app.models import Category, Item, User
from flask_login import login_user, logout_user
from flask import render_template, redirect, g, request, url_for
from flask import jsonify, flash, session as login_session, make_response


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


@app.route('/')
@app.route('/index/')
def showCatalog():

    categories = getDbSession().query(Category).all()
    latestItems = getDbSession().query(Item).order_by(Item.id.desc()).all()

    closeDbSession()

    return render_template('child_index.html',
                           categories=categories, latestItems=latestItems)


@app.route('/editItem', methods=['POST'])
def editItem():

    # check if item is authorized to be modified
    item = getDbSession().query(Item).filter_by(id=request.form['id']).one()

    print 'login session id '+login_session['id']
    print 'udser id '+item.user_id
    if login_session['id'] == item.user_id:
        print('Authorized')

        item = Item(request.form['id'], request.form['name'],
                request.form['description'], request.form['category'])
        update(item)
        return redirect("/index/")
    else:
        print('Not authorized')
        closeDbSession()
        flash('You are not authorized to edit this item.Please create your own item in order to edit.')
        return redirect("/index/")


@app.route('/addItem', methods=['POST'])
def addItem():
    if request.method == 'POST':
        item = Item(None, request.form['name'],
                    request.form['description'], request.form['category'],login_session['id'])
        add(item)
        return redirect("/index/")


@app.route('/itemDetails/<int:item_id>/')
def itemDetails(item_id):
    item = getDbSession().query(Item).filter_by(id=item_id).one()
    categories = getDbSession().query(Category).all()

    closeDbSession()

    return render_template('item_detail.html',
                           item=item, categories=categories)


# delete item by id
@app.route('/deleteItem/<int:item_id>/')
def deleteItem(item_id):

        # check if item is authorized to be modified
        item = getDbSession().query(Item).filter_by(id=item_id).one()

        if login_session['id'] == item.user_id:
            print('Authorized')

            deleteById(Item(), item_id)

            return redirect("/index/")
        else:
            print('Not authorized')
            closeDbSession()
            flash('You are not authorized to delete this item. Please create your own item in order to delete it.')
            return redirect("/index/")

''' callback function for reloading a user from the session
https://flask-login.readthedocs.io/en/latest/
#flask_login.LoginManager.user_loader'''


@login_manager.user_loader
def load_user(user_id):

    try:
        return User(1, login_session['name'],
                    login_session['picture'], login_session['email'])
    except:
        return None


# get category details
@app.route('/categoryDetails/<int:category_id>/')
def categoryDetails(category_id):
    category = getDbSession().query(Category).filter_by(id=category_id).one()
    items = getDbSession().query(Item).filter_by(category_id=category_id).all()

    closeDbSession()

    return render_template('category_details.html',
                           category=category, items=items)



@app.route('/getAddItemForm')
def getAddItemForm():

    return render_template('add_item_form.html')


# json endpoint
@app.route('/catalog/JSON')
def catalogJSON():
    categories = getDbSession().query(Category).order_by(Category.name).all()
    closeDbSession()
    return jsonify(Categories=[i.serialize for i in categories])


# json endpoint
@app.route('/catalog/<int:item_id>/JSON')
def catalogItemJSON(item_id):
    print("item id is "+str(item_id))
    item = getDbSession().query(Item).filter_by(id=item_id).one()
    closeDbSession()
    return jsonify(item.serialize)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:

        result = {'name': login_session['name']}
        jsonResult = json.dumps(result)
        console.log("Stored access token "+stored_access_token)
        login_user(User(1, login_session['name'],
                   login_session['picture'], login_session['email']))

        print("user is already logged int")

        return jsonResult

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    print(data['id'])

    state = ''.join(random.
                    choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))

    login_session['id'] = data['id']
    login_session['name'] = data['given_name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['state'] = state

    login_user(User(1, login_session['name'],
               login_session['picture'], login_session['email']))

    print("logged in user")
    return redirect("/index/")


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    print('check access token')

    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.
                                 dumps("""Current user
                                 not connected."""), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['name']
    oauth2Url = 'https://accounts.google.com/o/oauth2/revoke?token='
    url = oauth2Url + str(login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['name']
        del login_session['email']
        del login_session['picture']
        del login_session['state']

        logout_user()
        print 'Successfully disconnected.'
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print 'Error with disconnection'
        response = make_response(json.dumps("""Failed to revoke
                                             token for given user.""", 400))
        response.headers['Content-Type'] = 'application/json'
        return response
