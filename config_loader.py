from config import Config, load_smtp_config_from_db, save_smtp_config_to_db

def initialize_smtp_config(app):
    # Verificar si la configuración SMTP existe en las variables de entorno
    if not (Config.SMTP_SERVER and Config.SMTP_PORT and Config.EMAIL and Config.APP_PASS and Config.FROM and Config.FROM_NAME):
        # Si no existen en las variables de entorno, cargar desde la base de datos
        smtp_config = load_smtp_config_from_db()
        if smtp_config:
            app.config.update(smtp_config)
        else:
            print("No SMTP configuration found in environment variables or database.")
    else:
        # Si existen en las variables de entorno, guardar en la base de datos
        save_smtp_config_to_db()
        app.config.update({
            'SMTP_SERVER': Config.SMTP_SERVER,
            'SMTP_PORT': Config.SMTP_PORT,
            'EMAIL': Config.EMAIL,
            'APP_PASS': Config.APP_PASS,
            'FROM': Config.FROM,
            'FROM_NAME': Config.FROM_NAME
        })