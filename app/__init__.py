from flask import Flask
from config import Config
from config_loader import initialize_smtp_config
from .models import Base, engine

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    # Inicializar la base de datos
    with app.app_context():
        Base.metadata.create_all(engine)

    initialize_smtp_config(app)

    from .email_routes import email_bp
    app.register_blueprint(email_bp)

    return app
