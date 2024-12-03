from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class EmailForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    name=StringField("Name", validators=[DataRequired()])
    submit=SubmitField("Add email")

class ListForm(FlaskForm):
    name = StringField("List Name", validators=[DataRequired()])
    submit = SubmitField("Create List")

class AddToListForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    list_name = StringField("List Name", validators=[DataRequired()])
    submit = SubmitField("Add to List")