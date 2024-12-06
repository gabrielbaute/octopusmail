from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from ..forms import LoginForm, RegistrationForm
from ..models import User, Role
from ..db import session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        # Asignar el rol "User" por defecto
        user_role=session.query(Role).filter_by(name="User").first()
        if not user_role:
            flash("No se encontró el rol de usuario por defecto")
            return redirect(url_for("auth.register"))
        
        user=User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role_id=form.role.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('email.index'))
    form=LoginForm()
    if form.validate_on_submit():
        user=session.query(User).filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('email.index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))
