from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_email(subject, receiver_email, template_name, context):
    email_html_message = render_to_string(template_name, context)
    email = EmailMessage(
        subject,
        email_html_message,
        settings.ENV_VARIABLES['GMAIL_EMAIL'],
        [receiver_email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)
