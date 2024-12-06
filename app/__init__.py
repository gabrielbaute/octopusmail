from flask import Flask
from flask_login import LoginManager
from config import Config
from config_loader import initialize_smtp_config
from .models import Base, engine
from .initial_data import create_initial_admin, create_initial_roles

login_manager=LoginManager()
login_manager.login_view="auth.login"

@login_manager.user_loader
def load_user(user_id):
    from .db import session
    from .models import User
    return session.query(User).get(int(user_id))

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    login_manager.init_app(app)

    # Inicializar la base de datos
    with app.app_context():
        Base.metadata.create_all(engine)
        create_initial_roles()
        create_initial_admin()

    initialize_smtp_config(app)

    # Cargar los blueprint de las rutas
    from app.routes.email_routes import email_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.template_routes import templates_bp
    from app.routes.smtp_routes import smtp_bp
    app.register_blueprint(email_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(templates_bp)
    app.register_blueprint(smtp_bp)

    return app