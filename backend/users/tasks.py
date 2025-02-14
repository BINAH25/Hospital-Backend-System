from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from smtplib import SMTPException
from django.utils import timezone
from users.models import ActionableStep

@shared_task
def reduce_actionable_step_duration():
    """
    Runs daily at 6 AM to decrease ActionableStep duration by 1.
    If duration becomes 0, it stops updating the step.
    """
    today = timezone.now().date()
    steps = ActionableStep.objects.filter(step_type="Plan")

    for step in steps:
        if step.duration and int(step.duration) > 0:
            step.duration = str(int(step.duration) - 1)  # Reduce duration by 1
            step.save()

            if int(step.duration) == 0:
                print(f"Task {step.id} has completed. No further scheduling.")
