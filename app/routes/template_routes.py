import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required
from ..forms import TemplateUploadForm
from core.html_templates import make_html, write_html_from_user
from config import Config


templates_bp=Blueprint("templates", __name__)

# Ruta para mostrar el formulario de subida de plantillas HTML
@templates_bp.route("/upload_template", methods=["GET", "POST"])
@login_required
def upload_template():
    form=TemplateUploadForm()
    if form.validate_on_submit():
        template_name=form.template_name.data
        template_content = form.template_content.data

        # Crear el nombre del archivo con la extensión .html
        filepath=make_html(template_name)

        # Guardar el contenido HTML en el archivo
        write_html_from_user(template_content, filepath)
        
        flash("Template uploaded successfully!", "success")
        return redirect(url_for("email.upload_template"))
    
    return render_template("upload_template.html", form=form)

# Ruta para mostrar todas las plantillas
@templates_bp.route("/templates")
@login_required
def show_templates():
    templates=[]
    for filename in os.listdir(Config.TEMPLATE_DIR):
        if filename.endswith(".html"):
            templates.append(filename)
    return render_template('templates.html', templates=templates)

# Ruta para acceder al contenido de una plantilla
@templates_bp.route("/templates/<filename>")
@login_required
def get_template(filename):
    return send_from_directory(Config.TEMPLATE_DIR, filename)

# Ruta para editar el contenido de una plantilla
@templates_bp.route("/edit_template/<filename>", methods=["GET", "POST"])
@login_required
def edit_template(filename):
    filepath=os.path.join(Config.TEMPLATE_DIR, filename)
    form=TemplateUploadForm()

    if request.method == "POST" and form.validate_on_submit():
        template_content=form.template_content.data
        write_html_from_user(template_content, filepath)
        flash("Template updated successfully!", "success")
        return redirect(url_for("email.show_templates"))

    with open(filepath, 'r', encoding='utf-8') as file:
        form.template_name.data=filename.replace('.html', '')
        form.template_content.data=file.read()

    return render_template("edit_template.html", form=form, filename=filename)