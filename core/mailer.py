import os
from config import Config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

    
def headerCompose(receiver, subject):
    msg=MIMEMultipart()

    msg['From']=Config.FROM
    msg['To']=receiver
    msg['Subject']=subject

    return msg

def bodyCompose(templatepath, receiver_name, msg):
    with open(templatepath,'r', encoding='utf-8') as file:
        html_template=file.read()
    
    html_content=html_template.format(nombre=receiver_name)
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    return msg

def bodyCompose_with_content(template_content, receiver_name, msg):
    html_content = template_content.format(nombre=receiver_name)
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    return msg


def attachMedia(filepath, msg):
    with open(filepath, 'rb') as attachment:
        p=MIMEBase('aplication', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filepath)}')
        msg.attach(p)

    return msg