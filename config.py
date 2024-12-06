import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    DEBUG=os.getenv("DEBUG", "False").lower() in ["true", "1", "t"]
    HOST=os.getenv("HOST", "0.0.0.0")
    PORT=int(os.getenv("PORT", 5000))
    DATABASE_URL=os.getenv("DATABASE_URL")
    SECRET_KEY=os.getenv("SECRET_KEY")
    UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER")
    TEMPLATE_DIR=os.path.join(os.getcwd(), 'core', 'templates')

    # SMTP settings
    SMTP_SERVER=os.getenv("SMTP_SERVER")
    SMTP_PORT=int(os.getenv("SMTP_PORT"))
    EMAIL=os.getenv("EMAIL")
    APP_PASS=os.getenv("APP_PASS")
    FROM=os.getenv("FROM")

