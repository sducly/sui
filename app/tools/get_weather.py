import requests
from datetime import datetime
from langchain.tools import tool
import json

def get_coordinates(city_name):
    """
    Get the latitude and longitude of a city using the Open-Meteo Geocoding API.
    :param city_name: The name of the city.
    :return: A tuple containing latitude and longitude.
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=fr&format=json"
    response = requests.get(url)
    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        return data["results"][0]["latitude"], data["results"][0]["longitude"]
    else:
        raise ValueError(f"Ville '{city_name}' non trouvée.")

@tool
def get_weather(input_dict: dict):
    """
    Retourne la météo pour une ville donnée à une date spécifique.

    :param input_dict: Un dictionnaire contenant :
        - city_name (str) : Le nom de la ville recherchée. Obligatoire
        - date_iso (str) : La date recherchée au format ISO String. Obligatoire.

    :return: Un dictionnaire avec les conditions météos si l'appel a reussi sinon un message d'erreur
    """
    try:
        city_name = input_dict.get("city_name")
        date_iso = input_dict.get("date_iso")

        if not city_name or not date_iso:
            raise ValueError("Le JSON doit contenir les clés 'city_name' et 'date_iso'.")

        datetime.fromisoformat(date_iso)

    except (json.JSONDecodeError, TypeError, ValueError) as e:
        return {"error": f"Format incorrect : {str(e)}"}


    try:
        latitude, longitude = get_coordinates(city_name)

        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto&start_date={date_iso}&end_date={date_iso}"
        response = requests.get(url)
        data = response.json()

        if "daily" in data:
            return {
                "info": f"Météo pour la journée du {date_iso} à {city_name}",
                "city": city_name,
                "date": date_iso,
                "weather": "great sunny",
                "weather_code": data["daily"]["weathercode"][0],
                "max_temperature": data["daily"]["temperature_2m_max"][0],
                "min_temperature": data["daily"]["temperature_2m_min"][0],
            }
        else:
            return {"error": "Aucune donnée météo trouvée."}
    except Exception as e:
        return {"error": str(e)}
