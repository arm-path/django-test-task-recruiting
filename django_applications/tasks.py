from django.core.mail import send_mail

from django_settings.celery import app


@app.task
def send_email_enrolled(email, sith):
    """ Отправление письма на указанный email """
    try:
        send_mail(
            f'Орден ситхов, ситх {sith}',
            'Вы успешно зачислены в орден "Рук Тени"',
            '',  # TODO: Адрес электронной почты.
            [email],
            fail_silently=False, )
    except Exception as e:
        print('Error Send Mail', e)


@app.task
def send_email_excluded(email, sith):
    """ Отправление письма на указанный email """
    try:
        send_mail(
            f'Орден ситхов, ситх {sith}',
            'Вы исключены из ордена "Рук Тени"'
            '',  # TODO: Адрес электронной почты.
            [email],
            fail_silently=False, )
    except Exception:
        print('Error Send Mail')
