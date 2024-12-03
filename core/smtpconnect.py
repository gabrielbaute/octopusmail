import smtplib, os
from dotenv import load_dotenv

load_dotenv()
smtpserver=os.getenv("SMTP_SERVER")
smtpport=os.getenv("SMTP_PORT")
smtpmail=os.getenv("EMAIL")
password=os.getenv("APP_PASS")


server=smtplib.SMTP(smtpserver, smtpport)

def serverStart(server):
    try:
        server.ehlo()
        server.starttls()
        server.login(smtpmail, password)
        print('Inicio de sesión en SMTP exitoso')
    except smtplib.SMTPException as e:
        print(f'Error: No se pudo conectar: {e}')
        server.quit()

def serverQuiet(server):
    server.quit()