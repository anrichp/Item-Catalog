from flask import render_template, redirect, url_for, jsonify, session
from flask import request
from app import oauth2
from . import main
from .forms import NewItem, NewCategory, DeleteItem
from .. import db
from ..models import Category, Item


@main.route('/')
def index():
    categories = db.session.query(Category).all()
    items = db.session.query(Item).order_by(Item.created_date.desc()).all()
    return render_template('index.html', categories=categories, items=items)


# login route for oauth to trigger session['profile']
@main.route('/login')
@oauth2.required
def login():
    return redirect(url_for('.index'))


@main.route('/catalog/<category>/items')
def category(category):
    items = db.session.query(Item.name, Category.id).join(
        Category).filter(Category.name == category)
    categories = db.session.query(Category).all()
    return render_template('categoryItems.html', items=items,
                           categories=categories, category=category)


@main.route('/catalog/<category>/<item>')
def item(category, item):
    name = db.session.query(Item).filter_by(name=item).one()
    description = db.session.query(Item.description).filter_by(name=item).one()
    return render_template('item.html', name=name, description=description,
                           category=category)


@main.route('/catalog/newItem', methods=['GET', 'POST'])
@oauth2.required
def newItem():
    form = NewItem()
    if request.method == 'POST' and form.validate_on_submit():
        if 'profile' in session:
            item = Item(name=form.name.data,
                        description=form.description.data,
                        category=form.category.data,
                        createdById=session['profile']['email'],
                        createdBy=session['profile']['name'])
        else:
            return redirect(url_for('login'))
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('newItem.html', form=form)


@main.route('/catalog/newCategory', methods=['GET', 'POST'])
@oauth2.required
def newCategory():
    form = NewCategory()
    if request.method == 'POST' and form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('newCategory.html', form=form)


@main.route('/catalog/<category>/<item>/edit', methods=['GET', 'POST'])
@oauth2.required
def edit(category, item):
    description = db.session.query(Item.description).filter_by(name=item).one()
    categories = db.session.query(Category).all()
    editedItem = db.session.query(Item).filter_by(name=item).one()

    # convert query result to a string and remove unwanted characters
    description = str(description).replace("('", "").replace("',)", "")
    """
    receive form results and populate the Item object
    with updated information
    """
    if session['profile']['email'] != editedItem.createdById:
        render_template('editError.html')
    elif request.method == 'POST':
        editedItem.name = request.form['title']
        editedItem.description = request.form['description']
        editedItem.price = request.form['category']
        db.session.add(editedItem)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('editItem.html', item=item, description=description,
                           categories=categories, category=category)


@main.route('/catalog/<category>/<item>/delete', methods=['GET', 'POST'])
def delete(category, item):
    form = DeleteItem()
    deleteItem = db.session.query(Item).filter_by(name=item).first()
    # recieve delete instruction and ask for user input
    if request.method == 'POST':
        db.session.delete(deleteItem)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('delete.html', form=form, item=item)


# JSON endpoint for all items in the catalog
@main.route('/catalog/JSON')
def catalogJSON():
    catalog = db.session.query(Item).all()
    return jsonify(Item=[i.serialize for i in catalog])
