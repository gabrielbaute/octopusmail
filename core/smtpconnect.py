import smtplib, os
from config import Config

server=smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)

def serverStart(server):
    try:
        server.ehlo()
        server.starttls()
        server.login(Config.EMAIL, Config.APP_PASS)
        print("Inicio de sesión en SMTP exitoso")
    except smtplib.SMTPException as e:
        print(f"Error: No se pudo conectar: {e}")
        server.quit()

def serverQuit(server):
    server.quit()