from django.conf import settings
from apps.core import mail
from rotiapp.celery import app


def get_retry_channel():
    return getattr(settings, 'VENTA_MSG_RETRY_CHANNEL', None)


def base_send_message(subject, message, from_email, recipient_list, *args, **kwargs):    
    return mail.send_mail(subject, message, from_email, recipient_list, *args, **kwargs)


@app.task()
def send_message_async(subject, message, from_email, recipient_list, *args, **kwargs):
    return mail.send_mail(subject, message, from_email, recipient_list, *args, **kwargs)


def send_mail(subject, message, from_email, recipient_list, *args, **kwargs):
    
    if getattr(settings, 'CELERY_ENABLED', False):
        return send_message_async.delay(subject, message, from_email, recipient_list, *args, **kwargs)
    else:
        return base_send_message(subject, message, from_email, recipient_list, *args, **kwargs)



