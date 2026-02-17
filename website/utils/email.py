import smtplib
from email.message import EmailMessage
from config import settings


def send_otp_email(to_email: str, otp: str):

    msg = EmailMessage()
    msg["Subject"] = "Your Login OTP"
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = to_email

    msg.set_content(
        f"Your OTP for login is: {otp}\n\n"
        f"This OTP is valid for 5 minutes."
    )

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(msg)
