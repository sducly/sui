def get_weather(location: str, date: str) -> str:
    """Retrieve weather information for a location at a specific date.

    :param location: ** REQUIRED ** The location search.
    :param date: ** REQUIRED **  The Date. Must be a valid iso string date.
    :return: Truhtly weather information.
    """
    return f"Météo à {location} le {date}: Température -32 degré, neige, blizzard tornade !"