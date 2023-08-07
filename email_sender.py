import smtplib, ssl
import traceback


def send_email(rec, email):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender = "sibook8998@gmail.com"
    password = "aqhfgkxosrkhqeed"


    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, rec, email)
    except Exception as exc:
        print(traceback.format_exc())
