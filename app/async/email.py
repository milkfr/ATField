from flask import current_app, render_template
from flask_mail import Message
from app import mail, celery


@celery.task
def send_async_email(data):
    app = current_app._get_current_object()
    subject = data["subject"]
    to = data["to"]
    msg = Message(app.config["MAIL_SUBJECT_PREFIX"] + ' ' + subject,
                  sender=app.config["MAIL_SENDER"], recipients=[to])
    msg.body = data["body"]
    msg.html = data["html"]
    mail.send(msg)


def send_email(to, subject, template, **kwargs):
    data = {
        "to": to,
        "subject": subject,
        "body": render_template(template + ".txt", **kwargs),
        "html": render_template(template + ".html", **kwargs),
    }
    send_async_email.delay(data)
