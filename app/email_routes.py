import smtplib
import os
from werkzeug.utils import secure_filename
from flask import(
    Blueprint, 
    request, 
    jsonify, 
    render_template, 
    redirect, 
    url_for, 
    flash
    )

from core.importcsv import importcsv
from core.smtpconnect import serverStart, serverQuiet
from core.mailer import(headerCompose, bodyCompose, attachMedia) 

from config import Config
from .db import session
from .models import Email, List
from .forms import EmailForm, ListForm, AddToListForm, CSVUploadForm

email_bp=Blueprint("email", __name__)

@email_bp.route("/")
def index():
    return render_template("index.html")

@email_bp.route("/add_email", methods=["GET", "POST"])
def add_email():
    form=EmailForm()
    if form.validate_on_submit():
        existing_email=session.query(Email).filter_by(email=form.email.data).first()
        if existing_email:
            flash("Email already exists!", "danger")
        else:
            email=Email(email=form.email.data, name=form.name.data)
            session.add(email)
            session.commit()
            flash("Email added successfully!", "success")
        return redirect(url_for("email.add_email"))
    return render_template("add_email.html", form=form)

@email_bp.route("/create_list", methods=["GET", "POST"])
def create_list():
    form=ListForm()
    if form.validate_on_submit():
        existing_list=session.query(List).filter_by(name=form.name.data).first()
        if existing_list:
            flash("List name already exists!", "danger")
        else:
            email_list=List(name=form.name.data)
            session.add(email_list)
            session.commit()
            flash("List created successfully!", "success")
        return redirect(url_for("email.create_list"))
    return render_template("create_list.html", form=form)

@email_bp.route("/add_to_list", methods=["GET", "POST"])
def add_to_list():
    form=AddToListForm()
    if form.validate_on_submit():
        email=session.query(Email).filter_by(email=form.email.data).first()
        email_list=session.query(List).filter_by(name=form.list_name.data).first()
        if email in email_list:
            email.lists.append(email_list)
            session.commit()
            flash("Email added to list successfully!", "success")
            return redirect(url_for("email.add_to_list"))
        else:
            flash("Email or List not found", "danger")
    return render_template("add_to_list.html", form=form)

@email_bp.route("/upload_csv", methods=["GET", "POST"])
def upload_csv():
    form=CSVUploadForm()
    if form.validate_on_submit():
        # Almacenar el archivo .csv
        file=form.csv_file.data
        filename=secure_filename(file.filename)
        filepath=os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Leer el archivo .csv
        receivers=importcsv(filepath)
        list_name=form.list_name.data

        email_list=session.query(List).filter_by(name=list_name).first()
        if not email_list:
            email_list=List(name=list_name)
            session.add(email_list)
            session.commit()

        for receiver in receivers:
            if "email" in receiver and "name" in receiver:
                existing_email=session.query(Email).filter_by(email=receiver["email"]).first()
                if not existing_email:
                    email=Email(email=receiver["email"], name=receiver["name"])
                    session.add(email)
                    email.lists.append(email_list)
                else:
                    existing_email.lists.append(email_list)
            else:
                flash(f"Invalid data in row: {receiver}", "danger")
        session.commit()
        flash("CSV uploaded and emails added successfully!", "success")
        return redirect(url_for("email.upload_csv"))
    return render_template("upload_csv.html", form=form)

@email_bp.route("/send_email", methods=["POST"])
def send_email():
    data=request.json
    receivers=importcsv(data["csv_path"])

    server=smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
    serverStart(server)

    for receiver in receivers:
        msg=headerCompose(receiver["email"], data["subject"])
        msg=bodyCompose(data["template_path"], receiver["name"], msg)
        if "attachment_path" in data:
            msg=attachMedia(data["attachment_path"], msg)
        
        server.sendmail(Config.FROM, receiver["email"], msg.as_string())
    
    serverQuiet(server)

    return jsonify({"status": "success"}), 200
