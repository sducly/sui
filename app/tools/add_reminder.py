from langchain.tools import tool

@tool
def add_reminder(task: str, date: str) -> str:
    """Add a reminder for a certain task and at a specific date.

    :param task: What will be remind for the user. Required field
    :param date: When the reminder will be launch. The date must be a valid ISO String. Required field
    :return: A confirmation message.
    """
    return f"SUi a bien noté de rappeler {task} le {date}."