from django.core.mail import EmailMultiAlternatives


def send_email(email, subject, body):
    message = EmailMultiAlternatives(
        subject,
        body,
        to=[
            email,
        ],
    )
    message.send()
