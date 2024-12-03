import smtplib
from flask import(Blueprint, request, jsonify)

from core.importcsv import importcsv
from core.smtpconnect import serverStart, serverQuiet
from core.mailer import(headerCompose, bodyCompose, attachMedia) 

from config import Config
from .db import session
from .models import Email, List

email_bp=Blueprint("email", __name__)

@email_bp.route("/")
def index():
    return "<p>Hello, World!</p>"

@email_bp.route("/send_email", methods=["POST"])
def send_email():
    data=request.json
    receivers=importcsv(data["csv_path"])

    server=smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
    serverStart(server)

    for receiver in receivers:
        msg=headerCompose(receiver["email"], data["subject"])
        msg=bodyCompose(data["template_path"], receiver["name"], msg)
        if "attachment_path" in data:
            msg=attachMedia(data["attachment_path"], msg)
        
        server.sendmail(Config.FROM, receiver["email"], msg.as_string())
    
    serverQuiet(server)

    return jsonify({"status": "success"}), 200
