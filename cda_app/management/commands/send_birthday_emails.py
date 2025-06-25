from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import date
from cda_app.models import BirthdayCelebrant

class Command(BaseCommand):
    help = 'Sends birthday email alerts to admins for upcoming birthdays.'

    def handle(self, *args, **kwargs):
        today = date.today()
        # Get celebrants whose birthday is today
        celebrants = BirthdayCelebrant.objects.filter(
            date_of_birth__month=today.month,
            date_of_birth__day=today.day
        )

        if celebrants.exists():
            for celebrant in celebrants:
                subject = f'Happy Birthday {celebrant.name}!'
                html_message = render_to_string('emails/birthday_alert.html', {'celebrant': celebrant})
                plain_message = strip_tags(html_message)
                from_email = settings.DEFAULT_FROM_EMAIL
                # Replace with actual admin email or retrieve from settings/database
                recipient_list = [settings.ADMIN_EMAIL] 

                send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
                self.stdout.write(self.style.SUCCESS(f'Successfully sent birthday email for {celebrant.name}'))
        else:
            self.stdout.write(self.style.SUCCESS('No birthdays today.'))