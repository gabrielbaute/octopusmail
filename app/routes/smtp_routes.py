from flask import Blueprint, redirect, url_for, render_template, flash
from ..db import session
from ..models import SMTPProfile
from ..forms import SMTPProfileForm

smtp_bp=Blueprint("smtp", __name__)


# Ruta para mostrar todos los perfiles SMTP
@smtp_bp.route("/smtp_profiles")
def show_smtp_profiles():
    profiles = session.query(SMTPProfile).all()
    return render_template('smtp_profiles.html', profiles=profiles)

# Ruta para añadir un nuevo perfil SMTP
@smtp_bp.route("/add_smtp_profile", methods=["GET", "POST"])
def add_smtp_profile():
    form=SMTPProfileForm()
    if form.validate_on_submit():
        profile=SMTPProfile(
            service=form.service.data,
            port=form.port.data,
            email=form.email.data,
            app_pass=form.app_pass.data,
            from_name=form.from_name.data
        )
        session.add(profile)
        session.commit()
        flash("SMTP Profile added successfully!", "success")
        return redirect(url_for("smtp.show_smtp_profiles"))
    return render_template("add_smtp_profile.html", form=form)

# Ruta para editar un perfil SMTP existente
@smtp_bp.route("/edit_smtp_profile/<int:profile_id>", methods=["GET", "POST"])
def edit_smtp_profile(profile_id):
    profile=session.query(SMTPProfile).get(profile_id)
    form=SMTPProfileForm(obj=profile)
    if form.validate_on_submit():
        profile.service=form.service.data
        profile.port=form.port.data
        profile.email=form.email.data
        profile.app_pass=form.app_pass.data
        profile.from_name=form.from_name.data
        session.commit()
        flash("SMTP Profile updated successfully!", "success")
        return redirect(url_for("smtp.show_smtp_profiles"))
    return render_template("edit_smtp_profile.html", form=form)

# Ruta para eliminar un perfil SMTP existente
@smtp_bp.route("/delete_smtp_profile/<int:profile_id>", methods=["POST"])
def delete_smtp_profile(profile_id):
    profile=session.query(SMTPProfile).get(profile_id)
    session.delete(profile)
    session.commit()
    flash("SMTP Profile deleted successfully!", "success")
    return redirect(url_for("smtp.show_smtp_profiles"))