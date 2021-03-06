from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .. import db
from .. models import Category


# Query for QuerySelectField
def categoryQuery():
    return db.session.query(Category)


class NewItem(FlaskForm):
    name = StringField('Name', validators=[Length(0, 80), InputRequired()])
    description = StringField('Description', validators=[Length(0, 250),
                                                         InputRequired()])
    category = QuerySelectField(get_label='name', query_factory=categoryQuery)
    submit = SubmitField('Submit')


class NewCategory(FlaskForm):
    name = StringField('Name', validators=[Length(0, 64), InputRequired()])
    submit = SubmitField('Submit')


class DeleteItem(FlaskForm):
    delete = SubmitField('delete')
