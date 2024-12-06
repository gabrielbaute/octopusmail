from os.path import basename
from config import Config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formataddr
from email import encoders

    
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