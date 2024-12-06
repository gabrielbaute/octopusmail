from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

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
    list_name=StringField("List Name")
    existing_list=SelectField("Select Existing List", coerce=int)
    submit=SubmitField("Upload CSV")

class TemplateUploadForm(FlaskForm):
    template_name=StringField("Template Name", validators=[DataRequired()])
    template_content=TextAreaField("Template Content (HTML)", validators=[DataRequired()])
    submit=SubmitField("Upload Template")

class SMTPProfileForm(FlaskForm):
    service=SelectField(
        "SMTP Service",
        choices=[
            ("Google", "Google"),
            ("Outlook", "Outlook"),
            ("Yahoo", "Yahoo")],
        validators=[DataRequired()]
        )
    port = SelectField(
        "Port", 
        choices=[
            ("25", "25"), 
            ("465", "465"), 
            ("587", "587")
            ], 
        validators=[DataRequired()]
        )
    email=StringField("Email", validators=[DataRequired(), Email()])
    app_pass=StringField("App or mail pass", validators=[DataRequired()])
    from_name=StringField("From Name", validators=[DataRequired()])
    submit=SubmitField("Save")

class LoginForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired()])
    password=PasswordField("Password", validators=[DataRequired()])
    submit=SubmitField("Log In")

class RegistrationForm(FlaskForm):
    username=StringField("Username", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=PasswordField("Password", validators=[DataRequired()])
    password2=PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField("Register")