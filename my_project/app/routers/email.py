import smtplib
import ssl  # Import the ssl module
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

class EmailService:
    def __init__(self, smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str, tls_version: str = 'TLSv1_2'):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.tls_version = tls_version

    def send_email(self, recipients: List[str], subject: str, body: str):
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject

        # Attach body to the message
        msg.attach(MIMEText(body, 'plain'))

        # Establish SMTP connection
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls(context=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH))
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.smtp_username, recipients, msg.as_string())

# Initialize EmailService with your SMTP server details
email_service = EmailService(
    smtp_server='smtp.gmail.com',
    smtp_port=587,  # Update with your SMTP port
    smtp_username='maxwellmaina5194@gmail.com',
    smtp_password='dhum spii glde bvuh'
)