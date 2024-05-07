import logging

from django.core.mail import send_mail as django_send_mail


logger = logging.getLogger(__name__)


def send_mail(subject, message, from_email, recipient_list, *args, **kwargs):
    """
    Easy wrapper for sending a single message to a recipient list. All members
    of the recipient list will see the other recipients in the 'To' field.

    Usa el wrapper `send_mail` de django pero controlando el caso de que haya una excepcion
    silenciarla y que la misma se loggee. De esta manera no se abortan los procesos que envian mail.
    Por ejemplo que si el envio de email falla al solicitar un préstamo el proceso termine
    correctamente y no haga un rollback porque no pudo enviar el mail.
    """

    try:
        kwargs['fail_silently'] = kwargs.get('fail_silently', False)        
        return django_send_mail(subject, message, from_email, recipient_list, *args, **kwargs)
    except Exception:        
        logger.exception(f'Error en envio de email: {subject}')
        return 0
