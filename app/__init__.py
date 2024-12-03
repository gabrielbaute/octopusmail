from flask import Flask
from config import Config
from .models import Base, engine


def create_app():
    app=Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    from .email_routes import email_bp
    app.register_blueprint(email_bp)

    return app

def initialize_db():
    Base.metadata.create_all(engine)