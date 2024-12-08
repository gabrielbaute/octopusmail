import smtplib
import os
from werkzeug.utils import secure_filename
from flask_login import login_required
from flask import(
    Blueprint, 
    request,
    render_template, 
    redirect, 
    url_for, 
    flash
    )
from ..forms import ListForm, AddToListForm, EditListForm
from ..db import session
from ..models import List, Email

lists_bp=Blueprint("list", __name__)

@lists_bp.route("/create_list", methods=["GET", "POST"])
@login_required
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
        return redirect(url_for("list.create_list"))
    return render_template("create_list.html", form=form)

# Agregar correos a una lista, deprecated.
@lists_bp.route("/add_to_list", methods=["GET", "POST"])
@login_required
def add_to_list():
    form=AddToListForm()
    if form.validate_on_submit():
        email=session.query(Email).filter_by(email=form.email.data).first()
        email_list=session.query(List).filter_by(name=form.list_name.data).first()
        if email in email_list:
            email.lists.append(email_list)
            session.commit()
            flash("Email added to list successfully!", "success")
            return redirect(url_for("list.add_to_list"))
        else:
            flash("Email or List not found", "danger")
    return render_template("add_to_list.html", form=form)

# Ruta para mostrar las listas de correos
@lists_bp.route("/lists")
@login_required
def show_lists():
    lists=session.query(List).all()
    return render_template("list_list.html", lists=lists)

# Ruta para editar una lista
@lists_bp.route("/edit_list/<int:list_id>", methods=["GET", "POST"])
@login_required
def edit_list(list_id):
    email_list=session.query(List).get(list_id)
    form=EditListForm(obj=email_list)
    all_emails=session.query(Email).all()

    if form.validate_on_submit():
        email_list.name=form.name.data
        
        # Actualizar los correos en la lista
        selected_emails=request.form.getlist("emails")
        selected_email_objects=[session.query(Email).get(int(email_id)) for email_id in selected_emails]
        email_list.emails=selected_email_objects

        session.commit()
        flash("Lista actualizada correctamente.", "success")
        return redirect(url_for("list.show_lists"))
    
    return render_template("edit_list.html", form=form, all_emails=all_emails, email_list=email_list)

# Ruta para eliminar una lista
@lists_bp.route("/delete_list/<int:list_id>")
@login_required
def delete_list(list_id):
    email_list=session.query(List).get(list_id)
    session.delete(email_list)
    session.commit()
    flash("Lista eliminada correctamente.", "success")
    return redirect(url_for("list.show_lists"))

# Ruta para enviar correos a una lista específica
@lists_bp.route("/send_email_to_list/<string:list_name>")
@login_required
def send_email_to_list(list_name):
    return redirect(url_for("email.send_email_form", list_name=list_name))