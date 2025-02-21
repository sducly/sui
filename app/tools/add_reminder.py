def add_reminder(task: str, date: str) -> str:
    """Add a reminder for a certain task and at a specific date.

    :param task: ** REQUIRED ** What will be remind for the user.
    :param date: ** REQUIRED ** When the reminder will be launch. The date must be a valid ISO String.
    :return: A confirmation message.
    """
    return f"SUi a bien noté de rappeler {task} le {date}."