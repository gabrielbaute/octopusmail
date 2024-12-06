import smtplib
import os
from werkzeug.utils import secure_filename
from flask import(
    Blueprint, 
    request,
    render_template, 
    redirect, 
    url_for, 
    flash
    )

from core.importcsv import importcsv
from core.smtpconnect import(serverStart, serverQuit)
from core.mailer import(headerCompose, bodyCompose_with_content, attachMedia)
from core.html_templates import read_html_template

from config import Config
from ..db import session
from ..models import Email, List
from ..forms import EmailForm, ListForm, AddToListForm, CSVUploadForm

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
    lists=session.query(List).all()
    templates=[filename for filename in os.listdir(Config.TEMPLATE_DIR) if filename.endswith('.html')]
    return render_template("send_email.html", lists=lists, templates=templates)


# Ruta para enviar correos electrónicos
@email_bp.route("/send_email", methods=["POST"])
def send_email_route():
    send_mode=request.form.get("send_mode")
    subject=request.form.get("subject")
    template_filename=request.form.get("template_path")
    attachment_path=request.form.get("attachment_path")

    template_path = os.path.join(Config.TEMPLATE_DIR, template_filename)
    template_content = read_html_template(template_path)

    server_instance = serverStart()
    if not server_instance:
        flash("Failed to connect to SMTP server", "danger")
        return redirect(url_for("email.send_email_form"))

    try:
        if send_mode == "individual":
            receiver=request.form.get("receiver")
            receiver_name=request.form.get("receiver_name")
            msg=headerCompose(receiver, subject)
            msg=bodyCompose_with_content(template_content, receiver_name, msg)
            if attachment_path:
                msg=attachMedia(attachment_path, msg)
            server_instance.sendmail(msg['From'], msg['To'], msg.as_string())
        
        elif send_mode == "list":
            list_id=request.form.get("list_id")
            email_list=session.query(List).get(list_id)
            for email in email_list.emails:
                msg=headerCompose(email.email, subject)
                msg=bodyCompose_with_content(template_content, email.name, msg)
                if attachment_path:
                    msg=attachMedia(attachment_path, msg)
                server_instance.sendmail(msg['From'], msg['To'], msg.as_string())
        
        elif send_mode == "all":
            all_emails=session.query(Email).all()
            for email in all_emails:
                msg=headerCompose(email.email, subject)
                msg=bodyCompose_with_content(template_content, email.name, msg)
                if attachment_path:
                    msg=attachMedia(attachment_path, msg)
                server_instance.sendmail(msg['From'], msg['To'], msg.as_string())
        flash("Email sent successfully!", "success")
    except Exception as e:
        flash(f"Failed to send email: {e}", "danger")
    finally:
        serverQuit(server_instance)
    return redirect(url_for("email.show_emails"))

@email_bp.route("/emails")
def show_emails():
    emails=session.query(Email).all()
    return render_template("emails.html", emails=emails)