import os
import smtplib
from email.mime.text import MIMEText

SENDER = os.getenv('EMAIL_SENDER')
PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')

def send_auth_code(email, code):
    msg = MIMEText(f'Your authentication code is: {code}')
    msg['Subject'] = 'Authentication Code'
    msg['From'] = SENDER
    msg['To'] = email

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, email, msg.as_string())
