from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from cda_app.models import Defaulter

class Command(BaseCommand):
    help = 'Sends email alerts to admins for defaulters.'

    def handle(self, *args, **kwargs):
        defaulters = Defaulter.objects.filter(status='Indebt')

        if defaulters.exists():
            for defaulter in defaulters:
                subject = f'Defaulter Alert: {defaulter.name}'
                html_message = render_to_string('emails/defaulter_alert.html', {'defaulter': defaulter})
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                # Replace with actual admin email or retrieve from settings/database
                recipient_list = [settings.ADMIN_EMAIL] 

                send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
                self.stdout.write(self.style.SUCCESS(f'Successfully sent defaulter email for {defaulter.name}'))
        else:
            self.stdout.write(self.style.SUCCESS('No defaulters found.'))