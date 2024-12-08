from os.path import basename
from config import Config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formataddr
from email import encoders
from core.smtpconnect import serverStart, serverQuit
from core.html_templates import read_html_template
from app.models import Email, List
from app.db import session
    
def headerCompose(receiver, subject):
    msg=MIMEMultipart()
    from_adress=formataddr((Config.FROM_NAME, Config.EMAIL))

    msg['From']=from_adress
    msg['To']=receiver
    msg['Subject']=subject

    return msg

def bodyCompose(templatepath, receiver_name, msg):
    with open(templatepath,'r', encoding='utf-8') as file:
        html_template=file.read()
    
    html_content=html_template.format(receiver_name=receiver_name)
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    return msg

def bodyCompose_with_content(template_content, receiver_name, msg):
    try:
        # Reemplazar la variable {receiver_name} en el contenido de la plantilla
        html_content=template_content.format(receiver_name=receiver_name)
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    except KeyError as e:
        raise Exception(f"Failed to format template: {e}")
    
    return msg


def attachMedia(filepath, msg):
    with open(filepath, 'rb') as attachment:
        p=MIMEBase('aplication', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={basename(filepath)}')
        msg.attach(p)

    return msg

def send_scheduled_email(subject, template_path, attachment_path, send_mode, receiver, receiver_name, list_id):    

    template_content=read_html_template(template_path)
    server_instance=serverStart()
    
    if not server_instance:
        print("Failed to connect to SMTP server")
        return

    try:
        if send_mode == "individual":
            msg=headerCompose(receiver, subject)
            msg=bodyCompose_with_content(template_content, receiver_name, msg)
            if attachment_path:
                msg = attachMedia(attachment_path, msg)
            server_instance.sendmail(msg["From"], msg["To"], msg.as_string())

        elif send_mode == "list":
            email_list = session.query(List).get(list_id)
            for email in email_list.emails:
                msg=headerCompose(email.email, subject)
                msg=bodyCompose_with_content(template_content, email.name, msg)
                if attachment_path:
                    msg=attachMedia(attachment_path, msg)
                server_instance.sendmail(msg["From"], msg["To"], msg.as_string())

        elif send_mode == "all":
            all_emails=session.query(Email).all()
            for email in all_emails:
                msg=headerCompose(email.email, subject)
                msg=bodyCompose_with_content(template_content, email.name, msg)
                if attachment_path:
                    msg=attachMedia(attachment_path, msg)
                server_instance.sendmail(msg["From"], msg["To"], msg.as_string())

        print("Scheduled email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        serverQuit(server_instance) 