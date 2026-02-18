from email.message import EmailMessage
import smtplib
from config import settings

def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "Verify Your Account"
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = to_email

    msg.set_content(f"""
Your OTP for email verification is:

{otp}

This OTP is valid for 10 minutes.
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(msg)
