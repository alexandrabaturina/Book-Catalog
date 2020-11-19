from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Author, Book, User
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
engine = create_engine('sqlite:///books.db',
    connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

# Declare client ID
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def show_login():
    """
    Renders page to login with Google account.
    """
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# Server-side function to connect user to server.
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Connects authorized user to server.
    """
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

    # Check that the access token is valid
    access_token = credentials.access_token
    url = (f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user
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
        print("Token's client ID does not match the app's one.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Append name and email to login_session
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['access_token'] = credentials.access_token
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    return ''

# Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    """
    Disconnects user from server.
    """
    credentials = login_session.get('credentials')

    # Check if user is already disconnected
    if credentials is None:
        response = make_response(json.dumps(
                                'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token
    access_token = login_session['access_token']
    url = f"https://accounts.google.com/o/oauth2/revoke?token={access_token}"
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['access_token']

        response = make_response(json.dumps('Successfully Disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        response = make_response(json.dumps(
                                'Fail to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')

# JSON APIs
@app.route('/authors/<int:author_id>/JSON')
def show_author_json(author_id):
    """
    Takes author_id and returns info about all books of the author in JSON format.
    """
    books = session.query(Book).filter_by(author_id=author_id).all()
    return jsonify(books=[book.serialize for book in books])

@app.route('/authors/<int:author_id>/<int:book_id>/JSON')
def show_category_item_json(author_id, book_id):
    """
    Takes author_id and book_id and returns info about the book in JSON format.
    """
    book = session.query(Book).filter_by(author_id=author_id, id=book_id).one()
    return jsonify(book=book.serialize)

@app.route('/authors/JSON')
def show_authors_json():
    """
    Returns a list of authors.
    """
    authors = session.query(Author).all()
    return jsonify(authors=[author.serialize for author in authors])

# Show authors list
@app.route('/')
@app.route('/authors/')
def show_authors_list():
    """
    Renders a list of all authors.
    """
    authors = session.query(Author).order_by(Author.name).all()
    return render_template('authors-list.html', authors=authors)

# Add new author
@app.route('/author/new/', methods=['GET', 'POST'])
def add_author():
    """
    Handles data from "Add Author" form, adds new author to the database,
    and renders list of authors.
    """
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_authors_list'))
        if not request.form['new-author-name']:
            return render_template('add-author.html', empty_author_name=True)

        new_author = Author(
            name=request.form['new-author-name'],
            user_id = login_session['user_id'])
        session.add(new_author)
        session.commit()
        return redirect(url_for('show_authors_list'))
    else:
        return render_template('add-author.html')

# Edit author's name
@app.route('/author/<int:author_id>/edit/', methods=['GET', 'POST'])
def edit_author(author_id):
    """
    Takes author_id, edits author name with data from Edit Author form, and
    renders list of authors.
    """
    if 'username' not in login_session:
        return redirect('/login')

    author_to_edit = session.query(Author).filter_by(id=author_id).one()
    if request.method == 'POST':
        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_authors_list'))
        if not request.form['author-name']:
            return render_template(
                'edit-author.html',
                author=author_to_edit,
                empty_author_name=True)
        author_to_edit.name = request.form['author-name']
        return redirect(url_for('show_authors_list'))
    else:
        return render_template('edit-author.html', author=author_to_edit)

# Delete an author
@app.route('/author/<int:author_id>/delete/', methods=['GET', 'POST'])
def delete_author(author_id):
    """
    Takes author_id, removes the author with this id from database, and renders
    updated list of authors.
    """
    if 'username' not in login_session:
        return redirect('/login')
    author_to_delete = session.query(Author).filter_by(id=author_id).one()
    books_to_delete = session.query(Book).filter_by(author_id=author_id).all()

    if request.method == 'POST':
        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_authors_list', author_id=author_id))

        session.delete(author_to_delete)
        for book in books_to_delete:
            session.delete(book)
        session.commit()
        return redirect(
            url_for('show_authors_list', author_id=author_id))
    else:
        return render_template('delete-author.html', author=author_to_delete)

# Show a list of books for an author
@app.route('/author/<int:author_id>/')
@app.route('/author/<int:author_id>/books/')
def show_list(author_id):
    """
    Takes author_id and renders all books of the author with author_id.
    """
    author = session.query(Author).filter_by(id=author_id).one()
    books = session.query(Book).filter_by(author_id=author_id).order_by(Book.title).all()
    return render_template('books-list.html', books=books, author=author)

# Add new book
@app.route('/author/<int:author_id>/books/new/', methods=['GET', 'POST'])
def add_book(author_id):
    """
    Takes author_id, creates a new book using data from Add Book form
    in the database, and renders list of all books of the author with author_id.
    """
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':

        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_list', author_id=author_id))

        if not request.form['title-to-add']:
            return render_template('add-book.html',
                            author_id=author_id,
                            empty_title=True)
        new_book = Book(
            title=request.form['title-to-add'],
            description=request.form['description-to-add'],
            author_id=author_id,
            user_id=login_session['user_id'])
        session.add(new_book)
        session.commit()

        return redirect(url_for('show_list', author_id=author_id))
    else:
        return render_template('add-book.html', author_id=author_id)

# Edit book info
@app.route('/author/<int:author_id>/books/<int:book_id>/edit',
           methods=['GET', 'POST'])
def edit_book(author_id, book_id):
    """
    Takes author_id and book_id, edits the book with book_id using data from the
    Edit Book form, and renders all books of the author with author_id.
    """
    if 'username' not in login_session:
        return redirect('/login')
    book_to_edit = session.query(Book).filter_by(id=book_id).one()

    if request.method == 'POST':

        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_list', author_id=author_id))

        if not request.form['book-name']:
            return render_template('edit-book.html',
                                    book=book_to_edit,
                                    empty_title=True)
        if request.form['book-name']:
            book_to_edit.title = request.form['book-name']
        if request.form['description']:
            book_to_edit.description = request.form['description']
        else:
            book_to_edit.description = 'No description provided for this book yet.'
        session.add(book_to_edit)
        session.commit()
        return redirect(url_for('show_list', author_id=author_id))
    else:
        return render_template('edit-book.html',
                                author_id=author_id,
                                book=book_to_edit)

# Delete a book
@app.route('/author/<int:author_id>/books/<int:book_id>/delete',
           methods=['GET', 'POST'])
def delete_book(author_id, book_id):
    """
    Takes author_id and book_id, removes the book with book_id from the
    database, and renders all books of the author with author_id.
    """
    if 'username' not in login_session:
        return redirect('/login')
    book_to_delete = session.query(Book).filter_by(id=book_id).one()

    if request.method == 'POST':
        if request.form['submit-button'] == 'Cancel':
            return redirect(url_for('show_list', author_id=author_id))
        session.delete(book_to_delete)
        session.commit()
        return redirect(url_for('show_list', author_id=author_id))
    else:
        return render_template('delete-book.html', book=book_to_delete)

def get_user_id(email):
    """
    Takes user email and returns user id.
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def get_user_info(user_id):
    """
    Takes user_id and returns user information.
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Create a new user in the database
def create_user(login_session):
    """
    Takes session parameters login_session and creates new user.
    """
    new_user = User(
        name=login_session['username'],
        email=login_session['email'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

if __name__ == '__main__':
    app.secret_key = 'wnod21id90192djR222E2111ccqqqwjncnwi12111'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
