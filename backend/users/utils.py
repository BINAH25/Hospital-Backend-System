from google import genai
from django.conf import settings
import json
from datetime import timedelta
from django.utils import timezone
from .models import ActionableStep, Reminder
from django.utils.timezone import make_aware

# Set up Google Gemini API key
client = genai.Client(api_key="AIzaSyCxg04148E2GI7NA9eGJb7jYsZq-5eL_pg")  

def extract_actionable_steps(note_text):
    """
    Calls the Google Gemini API to extract actionable steps from a doctor's note.
    """
    prompt = f"""
    Extract actionable steps from the following doctor's note. Classify them into:
    - **Checklist**: Tasks that happen **only once** and do not repeat (e.g., "Take one dose of medicine", "Rest for the day").
    - **Plan**: Tasks that are **repeated over multiple days** (e.g., "Take medicine daily for 7 days").

    ### **Rules:**
    - If a task is for **only one day**, put it in **"Checklist"**.
    - If a task is for **more than one day**, put it in **"Plan"**.
    - If a medicine is prescribed **for multiple days**, it **must** go in **"Plan"** only.
    - Resting or any instruction **for just today** should **not be in the Plan**.

    ### **Doctor's Note:**
    {note_text}

    ### **Output Format (valid JSON):**
    {{
    "Checklist": ["task 1", "task 2", ...],
    "Plan": [
        {{"task": "task 1", "duration": "X days", "frequency": "daily/weekly/etc."}}, 
        ...
    ]
    }}
    """

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    try:
        # Extract response text properly
        json_text = response.text.strip("```json").strip("```") if hasattr(response, "text") else "{}"

        # Convert string to JSON
        result = json.loads(json_text)

        checklist = result.get("Checklist", [])
        plan = result.get("Plan", [])
    except json.JSONDecodeError:
        checklist, plan = [], []

    return checklist, plan



def process_plan_steps(note, plan_data):
    """
    Create Actionable Steps & Schedule Reminders based on Plan duration & frequency.
    """
    for task in plan_data:
        task_name = task["task"]
        duration_days = int(task["duration"].split()[0])  
        frequency = task.get("frequency", "daily")  

        step = ActionableStep.objects.create(
            note=note,
            step_type="Plan",
            description=task_name,
            scheduled_date = timezone.now().date(),
            frequency=frequency,  
            duration=duration_days 
        )

        # Schedule Reminders
        schedule_reminders(note.patient, step, duration_days, frequency)
        



def schedule_reminders(patient, step, duration_days, frequency):
    """
    Schedules reminders dynamically based on duration and frequency.
    """
    start_date = timezone.now()
    end_date = start_date + timedelta(days=duration_days)

    intervals = {
        "daily": 1,
        "twice a day": 0.5,  # Every 12 hours
        "weekly": 7
    }

    interval_days = intervals.get(frequency, 1)
    reminder_date = start_date

    while reminder_date <= end_date:
        Reminder.objects.create(
            patient=patient,
            actionable_step=step,
            scheduled_time=reminder_date
        )
        reminder_date += timedelta(days=interval_days)


def get_upcoming_reminders(patient):
    """
    Fetch upcoming reminders for a given patient.
    Only returns reminders that are scheduled for the future.
    """
    now = timezone.now()  # Ensure timezone-aware timestamp

    reminders = Reminder.objects.filter(
        patient=patient, 
        scheduled_time__gte=now,  # Only future reminders
        sent=False  # Exclude completed reminders
    ).order_by("scheduled_time")  # Order by upcoming date

    return reminders