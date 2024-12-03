from flask import Flask
from config import Config


def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    from .email_routes import email_bp
    app.register_blueprint(email_bp)

    return app