import sqlite3

def init_db():
    conn = sqlite3.connect("app/reminders.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            datetime TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_reminder(task, date):
    conn = sqlite3.connect("app.reminders.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (message, datetime) VALUES (?, ?)", (task, date))
    conn.commit()
    conn.close()
    return f"Ajout d'un rappel pour {task} le {date}."

def get_reminders():
    conn = sqlite3.connect("app.reminders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, message, datetime FROM reminders")
    reminders = cursor.fetchall()
    conn.close()
    return reminders

def delete_reminder(reminder_id):
    conn = sqlite3.connect("app.reminders.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()