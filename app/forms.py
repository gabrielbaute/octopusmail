from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Email

class EmailForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    name=StringField("Name", validators=[DataRequired()])
    submit=SubmitField("Add email")

class ListForm(FlaskForm):
    name=StringField("List Name", validators=[DataRequired()])
    submit=SubmitField("Create List")

class AddToListForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    list_name=StringField("List Name", validators=[DataRequired()])
    submit=SubmitField("Add to List")

class CSVUploadForm(FlaskForm):
    csv_file=FileField("CSV File", validators=[DataRequired()])
    list_name=StringField("List Name", validators=[DataRequired()])
    existing_list=SelectField("Select Existing List", coerce=int, validators=[DataRequired()])
    submit=SubmitField("Upload CSV")