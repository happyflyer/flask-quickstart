# -*- coding: utf-8 -*-

from threading import Thread

from flask import current_app
from flask_mail import Message

from . import mail


def _send_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, attachments=None):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    Thread(target=_send_email, args=(current_app._get_current_object(), msg)).start()
