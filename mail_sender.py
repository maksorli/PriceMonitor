import smtplib
from email.mime.text import MIMEText


def send_email(subject, body, to="recipient@example.com"):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "sender@example.com"
    msg["To"] = to

    with smtplib.SMTP("localhost") as server:  # подключить  MailCatcher
        server.sendmail("sender@example.com", [to], msg.as_string())
