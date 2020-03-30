from flask import Flask, render_template, request, redirect, jsonify
from flast import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem

engine = create_engine('sqlite:///catalogitems.db',
    connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# JSON APIs to view information
@app.route('/category/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return jsonify(CatalogItems=[i.serialize for i in items])


@app.route('/category/<int:category_id>/<int:item_id>/JSON')
def categoryItemJSON(category_id, item_id):
    Category_Item = session.query(CatalogItem).filter_by(id=item_id).one()
    return jsonify(Category_Item=Category_Item.serialize)


@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])

# Show all categories
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)

# Show a list of items in a category
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/list/')
def showList(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return render_template('list.html', items=items, category=category)

# Create a new category item
@app.route(
    '/category/<int:category_id>/list/new/', methods=['GET', 'POST'])
def newCatalogItem(category_id):
        if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'],
                            description=request.form['description'],
                            category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showList', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id)


# Edit a category item
@app.route('/category/<int:category_id>/list/<int:list_id>/edit',
           methods=['GET', 'POST'])
def editCatalogItem(category_id, list_id):
    editedItem = session.query(CatalogItem).filter_by(id=list_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showList', category_id=category_id))
    else:

        return render_template('edititem.html', category_id=category_id,
                                list_id=list_id, item=editedItem)

# Delete a category item
@app.route('/category/<int:category_id>/list/<int:list_id>/delete',
           methods=['GET', 'POST'])
def deleteCatalogItem(category_id, list_id):
    itemToDelete = session.query(CatalogItem).filter_by(id=list_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showList', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=itemToDelete)

app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
