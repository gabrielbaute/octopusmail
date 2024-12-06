import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    TEMPLATE_DIR = os.path.join(os.getcwd(), 'core', 'templates')
    
    # SMTP Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')
    EMAIL = os.getenv('EMAIL')
    APP_PASS = os.getenv('APP_PASS')
    FROM = os.getenv('FROM')
    FROM_NAME = os.getenv('FROM_NAME')

def load_smtp_config_from_db():
    from app.models import SMTPProfile
    from app.db import session
    
    profile = session.query(SMTPProfile).first()
    if profile:
        return {
            'SMTP_SERVER': {
                'Google': 'smtp.gmail.com',
                'Outlook': 'smtp-mail.outlook.com',
                'Yahoo': 'smtp.mail.yahoo.com'
            }.get(profile.service, profile.service),
            'SMTP_PORT': profile.port,
            'EMAIL': profile.email,
            'APP_PASS': profile.app_pass,
            'FROM': profile.email,
            'FROM_NAME': profile.from_name
        }
    return None

def save_smtp_config_to_db():
    from app.models import SMTPProfile
    from app.db import session
    
    profile = SMTPProfile(
        service='Google' if Config.SMTP_SERVER == 'smtp.gmail.com' else 'Outlook' if Config.SMTP_SERVER == 'smtp-mail.outlook.com' else 'Yahoo' if Config.SMTP_SERVER == 'smtp.mail.yahoo.com' else '',
        port=Config.SMTP_PORT,
        email=Config.EMAIL,
        app_pass=Config.APP_PASS,
        from_name=Config.FROM_NAME
    )
    session.add(profile)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error saving SMTP profile to database: {e}")