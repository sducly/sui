from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
from tools.reminder import get_reminders, delete_reminder
import requests

def check_reminders():
    """Vérifie les rappels et les déclenche au bon moment"""
    now = datetime.now(timezone.utc).isoformat()
    reminders = get_reminders()
    for reminder_id, message, reminder_time in reminders:
        if reminder_time <= now:
            # On envoie à Sui pour qu'il personnalise le rappel
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "sui", "prompt": f"Il est temps pour ce rappel : {message}. Dis-le avec ton style !", "stream": False}
            ).json()["response"]
            print("Rappel :", response)
            delete_reminder(reminder_id)

#scheduler = BackgroundScheduler()
#scheduler.add_job(check_reminders, "interval", seconds=30)
#scheduler.start()

check_reminders()
