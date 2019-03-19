from flask import render_template, redirect, url_for, jsonify, session
from flask import request
from app import oauth2
from . import main
from .forms import NewItem, NewCategory, DeleteItem
from .. import db
from ..models import Category, Item


@main.route('/')
def index():
    """Root decorator and index fucntion.
    Args:
        none.

    Retruns:
        index.html root page with categories and items.

    """
    categories = db.session.query(Category).all()
    items = db.session.query(Item).order_by(Item.created_date.desc()).all()
    return render_template('index.html', categories=categories, items=items)


@main.route('/login')
@oauth2.required
def login():
    """Login & oauth2 decorator to initiate Google API login.
    Args:
        none.

    Retruns:
        Redirect to index function after succesfull login.

    """
    return redirect(url_for('.index'))


@main.route('/catalog/<category>/items')
def category(category):
    """Category decorator and function to display all items in a category.
    Args:
        category (str): recieves category as string passing string
        to SQL Query.

    Retruns:
        render_template categories.html

    """
    items = db.session.query(Item.name, Category.id).join(
        Item).filter(Category.name == category)
    categories = db.session.query(Category).all()
    return render_template('categoryItems.html', items=items,
                           categories=categories, category=category)


@main.route('/catalog/<category>/<item>')
def item(category, item):
    """Item decorator and function to display an individual item
    Args:
        category (str): recieves category as string passing string to SQL Query
        item (str): receives item as a string passing string to SQL query.

    Retruns:
        render_template item.html displaying the individual
        item with descritption.

    """
    name = db.session.query(Item).filter_by(name=item).one()
    description = db.session.query(Item.description).filter_by(name=item).one()
    return render_template('item.html', name=name, description=description,
                           category=category)


@main.route('/catalog/newItem', methods=['GET', 'POST'])
@oauth2.required
def newItem():
    """New item decorator and function to create new item in DB
       @oauth2.required ensures that user is logged in.

    Retruns:
        ON GET:
            render_template with form to create new item
        ON POST:
            stores new item in database along with createdById
            and createdBy for user authentication at a later stage.
            redirects to index.


    """
    # Store WTForms object for newItem in form variable
    form = NewItem()
    if request.method == 'POST' and form.validate_on_submit():
        # determine whether user is logged in then store form items in DB
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
# decorator to ensure only logged in users have access to page
@oauth2.required
def newCategory():
    """New category decorator and function to create new category.
       @oauth2.required decorator ensures user is logged in.

    Retruns:
        ON GET:
            render_template newCategory.html with form.
        ON POST:
            New category is stored in DB and user is redirected to index.

    """
    # Store WTForms object for newCategory in form variable
    form = NewCategory()
    if request.method == 'POST' and form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('newCategory.html', form=form)


@main.route('/catalog/<category>/<item>/edit', methods=['GET', 'POST'])
# decorator to ensure only logged in users have access to page
@oauth2.required
def edit(category, item):
    """Edit decorator and function to return a form to edit the
       item passed to the function.
    Args:
        category (str): recieves category in order to construct URI.
        item (str): recieves item as a string passing string to SQL Query.

    Retruns:
        ON GET: IF statemnt evaluates whether the email address in the current
                session is not equal to the email address of the item in
                the DB, if the statement is True returns render_template
                editError.html indicating lack of permissions.

        ON POST:
            Stores edited details in DB and redirectes to the index.

    """
    description = db.session.query(Item.description).filter_by(name=item).one()
    categories = db.session.query(Category).all()
    editedItem = db.session.query(Item).filter_by(name=item).one()
    editor = db.session.query(Item.createdById).filter_by(name=item).one()
    # store current users email address in user_id variable
    user_id = session['profile']['email']
    # Determine whether the current user is the owner of the item
    if user_id != editor.createdById:
        return render_template('editError.html')
    else:
        if request.method == 'POST':
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
    """Delete decorator and function to return delete option on item
       passed to the function.
    Args:
        category (str): recieves category in order to construct URI.
        item (str): recieves item as a string passing string to SQL Query.

    Retruns:
        ON GET: IF statemnt evaluates whether the email address in the current
                session is not equal to the email address of the item in
                the DB, if the statement is True returns render_template
                editError.html indicating lack of permissions.

        ON POST:
            Triggers SQLAlchemy sesison to delete item, then redirects to index

    """
    # Store WTForms object for DeleteItem in form variable
    form = DeleteItem()
    deleteItem = db.session.query(Item).filter_by(name=item).first()
    editor = db.session.query(Item.createdById).filter_by(name=item).one()
    # store current users email address in user_id variable
    user_id = session['profile']['email']
    # Determine whether the current user is the owner of the item
    if user_id != editor.createdById:
        return render_template('deleteError.html')
    else:
        if request.method == 'POST':
            db.session.delete(deleteItem)
            db.session.commit()
            return redirect(url_for('.index'))
    return render_template('delete.html', form=form, item=item)


@main.route('/catalog/JSON')
def catalogJSON():
    """Catalog JSON decorator and fucntion serializing all catalog items
       to a JSON route

    Retruns:
        jasonified output of the entire catalog

    """
    catalog = db.session.query(Item).all()
    return jsonify(Item=[i.serialize for i in catalog])


@main.route('/catalog/<category>/<item>/JSON')
def itemJSON(category, item):
    """Catalog JSON decorator and fucntion serializing individual
       catalog items to a JSON route

    Retruns:
        jasonified output of an individual item in the  catalog

    """
    item = db.session.query(Item).filter_by(name=item).one()
    return jsonify(Item=[item.serialize])
