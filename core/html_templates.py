import os
from config import Config

def make_html(template_name):
    filename=f"{template_name}.html"
    filepath=os.path.join(Config.TEMPLATE_DIR, filename)

    return filepath

def write_html_from_user(template_content, filepath):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(template_content)
    
    return file