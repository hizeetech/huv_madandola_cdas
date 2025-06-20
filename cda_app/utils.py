from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_registration_email(user):
    subject = 'Registration Submitted - Madandola Estate CDA'
    html_message = render_to_string('emails/registration_submitted.html', {
        'user': user,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
    )

def send_approval_email(user):
    subject = 'Registration Approved - Madandola Estate CDA'
    html_message = render_to_string('emails/registration_approved.html', {
        'user': user,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
    )

def send_advert_created_email(advert):
    subject = 'Advert Created - Awaiting Approval'
    html_message = render_to_string('emails/advert_created.html', {
        'advert': advert,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [advert.user.email],
        html_message=html_message,
    )

def send_advert_approved_email(advert):
    subject = 'Advert Approved - Now Published'
    html_message = render_to_string('emails/advert_approved.html', {
        'advert': advert,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [advert.user.email],
        html_message=html_message,
    )

def send_donation_proof_email(donation_proof):
    subject = 'New Donation Proof Submitted'
    html_message = render_to_string('emails/donation_proof.html', {
        'proof': donation_proof,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],  # Send to admin
        html_message=html_message,
    )
    
    
# cda_app/utils.py

def send_payment_proof_email(levy, user):
    subject = 'Payment Proof Uploaded'
    html_message = render_to_string('emails/payment_proof_uploaded.html', {
        'levy': levy,
        'user': user
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
    )

def send_payment_approved_email(levy):
    subject = 'Payment Approved'
    html_message = render_to_string('emails/payment_approved.html', {
        'levy': levy
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [levy.user.email],
        html_message=html_message,
    )

def send_payment_rejected_email(levy):
    subject = 'Payment Rejected'
    html_message = render_to_string('emails/payment_rejected.html', {
        'levy': levy
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [levy.user.email],
        html_message=html_message,
    )