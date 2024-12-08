from flask import Blueprint
from .auth_routes import auth_bp
from .email_routes import email_bp
from .lists_routes import lists_bp
from .smtp_routes import smtp_bp
from .template_routes import templates_bp
from .tracking_routes import tracking_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(email_bp)
    app.register_blueprint(lists_bp)
    app.register_blueprint(smtp_bp)
    app.register_blueprint(templates_bp)
    app.register_blueprint(tracking_bp)