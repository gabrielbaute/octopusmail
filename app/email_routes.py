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
from core.smtpconnect import(server, serverStart, serverQuit)
from core.mailer import(headerCompose, bodyCompose, attachMedia) 

from config import Config
from .db import session
from .models import Email, List
from .forms import EmailForm, ListForm, AddToListForm, CSVUploadForm, TemplateUploadForm

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
    form = CSVUploadForm()
    
    # Poblar el campo de selección con listas existentes
    form.existing_list.choices=[(l.id, l.name) for l in session.query(List).all()]

    if form.validate_on_submit():
	    # Almacenar el archivo .csv
        file=form.csv_file.data
        filename=secure_filename(file.filename)
        filepath=os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        receivers=importcsv(filepath)
        
        list_name=form.list_name.data
        existing_list_id=form.existing_list.data

        # Crear una nueva lista si se ha proporcionado un nombre de lista nuevo
        if list_name:
            email_list=session.query(List).filter_by(name=list_name).first()
            if not email_list:
                email_list=List(name=list_name)
                session.add(email_list)
                session.commit()
	    # Usar lista existente
        else:
            email_list=session.query(List).get(existing_list_id)

        for receiver in receivers:
            print(f"Processing receiver: {receiver}") # Depuración
            if "email" in receiver and "name" in receiver:
                existing_email=session.query(Email).filter_by(email=receiver["email"]).first()
                if not existing_email:
                    email=Email(email=receiver["email"], name=receiver["name"])
                    session.add(email)
      		    
	            # Asignar el correo a la lista
                    email.lists.append(email_list)
                    print(f"Added email: {email.email}") # Depuración
                else:
                    existing_email.lists.append(email_list)
                    print(f"Updated existing email: {existing_email.email}") # Depuración
            else:
                flash(f"Invalid data in row: {receiver}", "danger")
        session.commit()
        flash("CSV uploaded and emails added successfully!", "success")
        return redirect(url_for("email.upload_csv"))
    
    return render_template("upload_csv.html", form=form)

# Ruta para mostrar el formulario de envío de correos electrónicos
@email_bp.route("/send_email_form", methods=["GET"])
def send_email_form():
    lists = session.query(List).all()
    return render_template("send_email.html", lists=lists)


# Ruta para enviar correos electrónicos
@email_bp.route("/send_email", methods=["POST"])
def send_email_route():
    send_mode=request.form.get("send_mode")
    subject=request.form.get("subject")
    template_path=request.form.get("template_path")
    receiver_name=request.form.get("receiver_name")
    attachment_path=request.form.get("attachment_path")

    if send_mode == "individual":
        receiver=request.form.get("receiver")
        msg=headerCompose(receiver, subject)
        msg=bodyCompose(template_path, receiver_name, msg)
        if attachment_path:
            msg=attachMedia(attachment_path, msg)
        serverStart(server)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        serverQuit(server)
    
    elif send_mode == "list":
        list_id=request.form.get("list_id")
        email_list=session.query(List).get(list_id)
        serverStart(server)
        for email in email_list.emails:
            msg=headerCompose(email.email, subject)
            msg=bodyCompose(template_path, email.name, msg)
            if attachment_path:
                msg=attachMedia(attachment_path, msg)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        serverQuit(server)
    
    elif send_mode == "all":
        all_emails=session.query(Email).all()
        serverStart(server)
        for email in all_emails:
            msg=headerCompose(email.email, subject)
            msg=bodyCompose(template_path, email.name, msg)
            if attachment_path:
                msg=attachMedia(attachment_path, msg)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        serverQuit(server)
    
    flash("Email sent successfully!", "success")
    return redirect(url_for("email.show_emails"))

@email_bp.route("/emails")
def show_emails():
    emails=session.query(Email).all()
    return render_template("emails.html", emails=emails)

# Ruta para mostrar el formulario de subida de plantillas HTML
@email_bp.route("/upload_template", methods=["GET", "POST"])
def upload_template():
    form=TemplateUploadForm()
    if form.validate_on_submit():
        template_name=form.template_name.data
        template_content = form.template_content.data

        # Crear el nombre del archivo con la extensión .html
        filename=f"{template_name}.html"
        filepath=os.path.join(Config.TEMPLATE_DIR, filename)

        # Guardar el contenido HTML en el archivo
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(template_content)
        
        flash("Template uploaded successfully!", "success")
        return redirect(url_for("email.upload_template"))
    
    return render_template("upload_template.html", form=form)