import smtplib
from config import Config

def serverStart():
    try:
        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(Config.EMAIL, Config.APP_PASS)
        return server
    except smtplib.SMTPException as e:
        print(f"Error: No se pudo conectar: {e}")
        return None

def serverQuit(server):
    try:
        server.quit()
    except smtplib.SMTPException as e:
        print(f"Error al cerrar la conexión SMTP: {e}")

# Función de verificación manual, útil para pruebas
def verify_smtp_connection():
    server = serverStart()
    if server:
        serverQuit(server)
    else:
        print("No se pudo establecer la conexión SMTP")

if __name__ == "__main__":
    verify_smtp_connection()
