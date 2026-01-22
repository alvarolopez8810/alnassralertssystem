import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_JEFE = os.getenv('EMAIL_JEFE', 'al.scoutinglab@gmail.com')

EMAIL_DESTINATARIOS = [
    EMAIL_JEFE
]
