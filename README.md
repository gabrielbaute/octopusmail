# OctopusMail 📧🐙

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-1.1.2-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.3.23-red.svg)
![Bulma](https://img.shields.io/badge/Bulma-0.9.3-lightgreen.svg)

Esta es una aplicación de envío de correos utilizando Flask, SQLAlchemy y Bulma. La aplicación permite gestionar correos electrónicos y listas de correos, cargar contactos desde archivos CSV, y enviar correos electrónicos a listas específicas.

## Características
- ✉️ Añadir correos electrónicos de manera individual.
- 📝 Crear y gestionar listas de correos.
- 📧 Añadir correos electrónicos a listas existentes.
- 📂 Cargar contactos desde archivos CSV y asignarlos a listas.
- 🔑 Login
- 📤 Enviar correos de forma masiva o por listas
- ⏰ Programar envío de correos
- 📊 Pixel de seguimiento
- 📈 Registro de métricas de envío de correos

## Instalación
1. Clona el repositorio:
    ```bash
    git clone https://github.com/gabrielbaute/octopusmail
    cd octopusmail
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

    #### Flask Settings

    | Variable        | Valor por Defecto                     | Descripción                                                                 |
    |-----------------|---------------------------------------|-----------------------------------------------------------------------------|
    | `SECRET_KEY`    | `mysecretkey`                         | Clave secreta utilizada por Flask para mantener la seguridad de la sesión.  |
    | `DATABASE_URL`  | `sqlite:///emails.db`             | URL de la base de datos. Ejemplo: `sqlite:///mydatabase.db` o `postgresql://user:password@localhost/mydatabase` |
    | `DEBUG`         | `False`                               | Modo de depuración. Opciones: `True`, `False`.                              |
    | `HOST`          | `0.0.0.0`                             | Dirección de host en la que se ejecuta la aplicación.                       |
    | `PORT`          | `5000`                                | Puerto en el que se ejecuta la aplicación.                                  |
    | `UPLOAD_FOLDER` | `None`                                | Ruta del directorio de subida de archivos.                                  |
    | `TEMPLATE_DIR`  | `os.path.join(os.getcwd(), 'core', 'templates')` | Directorio de plantillas de la aplicación.                                  |
    | `TZ`            | `America/Caracas`                     | Zona horaria del servidor                            |

    #### SMTP Settings

    | Variable        | Valor por Defecto | Descripción                                                                 |
    |-----------------|-------------------|-----------------------------------------------------------------------------|
    | `SMTP_SERVER`   | `None`            | Dirección del servidor SMTP. Ejemplo: `smtp.gmail.com`.                      |
    | `SMTP_PORT`     | `None`            | Puerto del servidor SMTP. Ejemplo: `587` para TLS, `465` para SSL.          |
    | `EMAIL`         | `None`            | Correo electrónico utilizado para enviar correos.                           |
    | `APP_PASS`      | `None`            | Contraseña de la aplicación o token para el correo electrónico.             |
    | `FROM`          | `None`            | Dirección de correo desde la cual se enviarán los correos.                   |
    | `FROM_NAME`     | `None`            | Nombre del remitente de los correos.                                         |

    ### Ejemplo de Configuración del Archivo `.env`

    Asegúrate de crear un archivo `.env` con las variables necesarias. Aquí hay un ejemplo:

    ```env
    SECRET_KEY=mysecretkey
    DATABASE_URL=sqlite:///mydatabase.db
    DEBUG=True
    HOST=0.0.0.0
    PORT=5000
    UPLOAD_FOLDER=./uploads
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    EMAIL=tu_correo@gmail.com
    APP_PASS=tu_app_pass
    FROM=tu_correo@gmail.com
    FROM_NAME=Tu Nombre
    ```

5. Ejecuta la aplicación:
    ```bash
    python run.py
    ```

### Credenciales del Admin por Defecto

El sistema inicializa un usuario administrador con las siguientes credenciales por defecto:

- **Nombre de usuario**: `admin`
- **Correo electrónico**: `admin@example.com`
- **Contraseña**: `adminpassword`

Por favor, cambia estas credenciales después del primer inicio de sesión para mantener la seguridad del sistema.

## Uso
- Navega a `http://127.0.0.1:5000/` (o el puerto que hayas especificado) en tu navegador.
- Utiliza la interfaz para añadir correos, crear listas, y cargar contactos desde archivos CSV.

## Contribuir
1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz un commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Empuja tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.