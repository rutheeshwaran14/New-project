from email.message import EmailMessage
import smtplib
from config import SMTP_EMAIL, SMTP_PASSWORD

def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "Verify Your Account"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    msg.set_content(f"""
Your OTP for email verification is:

{otp}

This OTP is valid for 10 minutes.
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
