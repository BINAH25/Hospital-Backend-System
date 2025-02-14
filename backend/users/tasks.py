from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException
from django.utils import timezone
from users.models import ActionableStep

@shared_task
def reduce_actionable_step_duration():
    """
    Runs daily at 6 AM to decrease ActionableStep duration by 1.
    If duration becomes 0, it stops updating the step.
    Sends an email reminder to the patient.
    """
    steps = ActionableStep.objects.filter(step_type="Plan")

    for step in steps:
        if step.duration and int(step.duration) > 0:
            step.duration = str(int(step.duration) - 1)  
            step.save()

            # Send email reminder
            send_email_reminder(step)


def send_email_reminder(step):
    """
    Sends an email reminder to the patient about their actionable step.
    """
    patient_email = step.note.patient.email
    if patient_email:     
        subject = "Reminder: Your Actionable Step for Today"
        message = f"Hello {step.note.patient.name},\n\nThis is a reminder to complete: {step.description}.\n\nRegards,\nYour Health System"
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [patient_email],
            fail_silently=False,
        )