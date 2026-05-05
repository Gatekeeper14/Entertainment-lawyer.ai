from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def send_email(to_email, content):
    message = Mail(
        from_email='noreply@entlawyer.ai',
        to_emails=to_email,
        subject='Your Contract Analysis',
        html_content=content
    )

    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    sg.send(message)
