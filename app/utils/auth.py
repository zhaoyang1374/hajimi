import os
import app.config.settings as settings

def verify_web_password(password:str):
    if password != settings.WEB_PASSWORD:
        return False
    return True