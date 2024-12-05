# MailServer Application

## Descripción
Esta es una aplicación de envío de correos utilizando Flask, SQLAlchemy y Bulma. La aplicación permite gestionar correos electrónicos y listas de correos, cargar contactos desde archivos CSV, y enviar correos electrónicos a listas específicas.

## Características
- Añadir correos electrónicos de manera individual.
- Crear y gestionar listas de correos.
- Añadir correos electrónicos a listas existentes.
- Cargar contactos desde archivos CSV y asignarlos a listas.
- Interfaz de usuario elegante utilizando Bulma CSS.

## Requisitos
- Python 3.x
- Flask
- SQLAlchemy
- Flask-WTF
- WTForms
- email-validator
- dotenv

## Instalación
1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu_usuario/mailserver.git
    cd mailserver
    ```

2. Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno:
    Crea un archivo `.env` en el directorio raíz del proyecto y añade las siguientes variables:
    ```ini
    SECRET_KEY=tu_clave_secreta
    DATABASE_URL=sqlite:///emails.db
    SMTP_SERVER=tu_smtp_server
    SMTP_PORT=tu_smtp_port
    EMAIL=tu_email
    APP_PASS=tu_contraseña_de_app
    FROM=tu_email
    ```

5. Crea las tablas de la base de datos:
    ```bash
    flask shell
    >>> from app import initialize_db
    >>> initialize_db()
    >>> exit()
    ```

6. Ejecuta la aplicación:
    ```bash
    flask run
    ```

## Uso
- Navega a `http://127.0.0.1:5000/` en tu navegador.
- Utiliza la interfaz para añadir correos, crear listas, y cargar contactos desde archivos CSV.

## Estructura del Proyecto
```
mailserver/
├── app/
│   ├── __init__.py
│   ├── email_routes.py
│   ├── forms.py
│   ├── models.py
│   ├── templates/
│   ├── static/
│       ├── css/
│       └── js/
├── core/
│   ├── __init__.py
│   └── importcsv.py
├── uploads/
├── config.py
├── db.py
├── run.py
└── .env
```

## Contribuir
1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz un commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Empuja tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.