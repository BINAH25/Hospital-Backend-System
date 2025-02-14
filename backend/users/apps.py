from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        """
        Ensures that the periodic task for reducing actionable step duration
        is created when the app starts.
        """
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        from django.db.utils import OperationalError, ProgrammingError
        import json

        try:
            # Create or get a Crontab schedule for 6 AM daily
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute="0",
                hour="6",
                day_of_week="*",   # Every day
                day_of_month="*",  # Every day of the month
                month_of_year="*", # Every month
            )

            # Ensure the periodic task exists
            task_name = "Reduce Actionable Step Duration"
            task, created = PeriodicTask.objects.get_or_create(
                name=task_name,
                defaults={
                    "crontab": schedule,
                    "task": "users.tasks.reduce_actionable_step_duration",
                    "args": json.dumps([]),  # No arguments needed
                    "enabled": True,
                },
            )

            if not created:
                # Update existing task if needed
                task.crontab = schedule
                task.enabled = True
                task.save()

        except (OperationalError, ProgrammingError):
            # Avoid breaking the app if database migrations are not applied yet
            pass
