from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem, User
from flask import session as login_session

from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets

import random
import string
import json
import httplib2
import requests

app = Flask(__name__)

# Connect to database and create database session
engine = create_engine('sqlite:///catalogitems.db',
    connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

# Declare client ID
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# Create server side function
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Connect user to server."""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
                                json.dumps(
                                    'Current user is already connected.'),
                                200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # append name, picture and email to login_session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['access_token'] = credentials.access_token
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:'
    output += ' 150px;-webkit-border-radius: 150px;'
    output += ' -moz-border-radius: 150px;"> '
    return output

# Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    """Disconnect user from server."""

    credentials = login_session.get('credentials')
    # check if user is already disconnected
    if credentials is None:
        response = make_response(json.dumps(
                                'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['access_token']

        response = make_response(json.dumps('Successfully Disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
#        return redirect(url_for('showLogin'))
        return redirect('/')
    else:
        response = make_response(json.dumps(
                                'Fail to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        #return redirect(url_for('showLogin'))
        return redirect('/')


# JSON APIs to view information
@app.route('/category/<int:category_id>/JSON')
def show_category_json(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return jsonify(CatalogItems=[i.serialize for i in items])


@app.route('/category/<int:category_id>/<int:item_id>/JSON')
def show_category_item_json(category_id, item_id):
    Category_Item = session.query(CatalogItem).filter_by(id=item_id).one()
    return jsonify(Category_Item=Category_Item.serialize)


@app.route('/category/JSON')
def show_categories_json():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# Show all categories
@app.route('/')
@app.route('/category/')
def show_categories():
    categories = session.query(Category).order_by(Category.name).all()
    return render_template('authors-list.html', categories=categories)


# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
def add_category():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':

        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_categories'))

        if not request.form['new-author-name']:
            return render_template('add-author.html', empty_author_name=True)

        newCategory = Category(name=request.form['new-author-name'],
                                user_id = login_session['user_id'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('show_categories'))
    else:
        return render_template('add-author.html')


# Edit a category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def edit_category(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_categories'))
        if not request.form['author-name']:
            return render_template('edit-author.html', category=editedCategory, editing_error=True)
        editedCategory.name = request.form['author-name']
        return redirect(url_for('show_categories'))
    else:
        return render_template('edit-author.html', category=editedCategory)


# Delete a category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def delete_category(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()

    if request.method == 'POST':
        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_categories', category_id=category_id))
        session.delete(categoryToDelete)
        session.commit()
        return redirect(
            url_for('show_categories', category_id=category_id))
    else:
        return render_template(
            'delete-author.html', category=categoryToDelete)

# Show a list of items in a category
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/list/')
def show_list(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).order_by(CatalogItem.name).all()
    return render_template('books-list.html', items=items, category=category)

# Create a new category item
@app.route(
    '/category/<int:category_id>/list/new/', methods=['GET', 'POST'])
def add_catalog_item(category_id):
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':

        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_list', category_id=category_id))

        if not request.form['title-to-add']:
            return render_template('add-book.html',
                            category_id=category_id,
                            empty_title=True)

        newItem = CatalogItem(name=request.form['title-to-add'],
                            description=request.form['description-to-add'],
                            category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('show_list', category_id=category_id))
    else:
        return render_template('add-book.html', category_id=category_id)


# Edit a category item
@app.route('/category/<int:category_id>/list/<int:list_id>/edit',
           methods=['GET', 'POST'])
def edit_catalog_item(category_id, list_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(CatalogItem).filter_by(id=list_id).one()

    if request.method == 'POST':

        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_list', category_id=category_id))

        if not request.form['book-name']:
            return render_template('edit-book.html',
                                    category_id=category_id,
                                    list_id=list_id,
                                    item=editedItem,
                                    error_title=True)
        if request.form['book-name']:
            editedItem.name = request.form['book-name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('show_list', category_id=category_id))
    else:

        return render_template('edit-book.html',
                                category_id=category_id,
                                list_id=list_id,
                                item=editedItem)


# Delete a category item
@app.route('/category/<int:category_id>/list/<int:list_id>/delete',
           methods=['GET', 'POST'])
def delete_catalog_item(category_id, list_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(CatalogItem).filter_by(id=list_id).one()

    if request.method == 'POST':
        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_list', category_id=category_id))

        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('show_list', category_id=category_id))
    else:
        return render_template('delete-book.html', item=itemToDelete)

def get_user_id(email):
    """Get user id."""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def get_user_info(user_id):
    """Get user information."""
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Create a new user in the database
def create_user(login_session):
    """Create a user."""
    newUser = User(
                    name=login_session['username'],
                    email=login_session['email'],
                    picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

if __name__ == '__main__':
    app.secret_key = 'wnod21id90192djR222E2111ccqqqwjncnwi12111'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
