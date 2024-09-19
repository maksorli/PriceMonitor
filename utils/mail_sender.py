import smtplib
from email.mime.text import MIMEText


def send_email(subject, body, to="crypto@boy.com"):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "crypto@monitor.com"
    msg["To"] = to

    with smtplib.SMTP("mailcatcher", 1025) as server:  # подключить  MailCatcher
        server.sendmail("crypto@monitor.com", [to], msg.as_string())
