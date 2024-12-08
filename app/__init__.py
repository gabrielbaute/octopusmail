import atexit
from flask import Flask
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from config_loader import initialize_smtp_config
from .models import Base, engine, Email, User, List
from .db import session
from .initial_data import create_initial_admin, create_initial_roles

login_manager=LoginManager()
login_manager.login_view="auth.login"

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

def send_scheduled_email():
    # Lógica para enviar un correo programado. Ejemplo: enviar un correo a una lista específica
    email_list=session.query(List).first()  # Seleccionar una lista de ejemplo
    if email_list:
        for email in email_list.emails:
            print(f"Enviando correo a {email.email}")
            # Aquí iría la lógica para enviar el correo

def create_app():
    app=Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    login_manager.init_app(app)

    # Inicializar la base de datos
    with app.app_context():
        Base.metadata.create_all(engine)
        create_initial_roles()
        create_initial_admin()

    initialize_smtp_config(app)

    # Configurar APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_scheduled_email, trigger="interval", minutes=1)  # Programar para ejecutar cada minuto
    scheduler.start()

    # Asegurarse de que el scheduler se detiene cuando se cierra la aplicación
    atexit.register(lambda: scheduler.shutdown())

    # Carga de los blueprints de enrutamiento
    from app.routes import register_blueprints
    register_blueprints(app)

    return app