from flask import Blueprint, render_template
from flask_login import login_required
from ..db import session
from ..models import Email, List

tracking_bp=Blueprint("tracking", __name__)

# Ruta para el pixel de seguimiento
@tracking_bp.route('/track_open/<int:email_id>')
def track_open(email_id):
    email=session.query(Email).get(email_id)
    email.open_count += 1  # Incrementar el contador de aperturas
    session.commit()
    return '', 204  # Responder con un status 204 No Content

# Ruta para mostrar las estadísticas de seguimiento
@tracking_bp.route("/tracking_statistics")
@login_required
def tracking_statistics():
    emails=session.query(Email).all()
    lists=session.query(List).all()
    return render_template("tracking_statistics.html", emails=emails, lists=lists)