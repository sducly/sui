import json

from core.tts import speak
from core.ai_stream import create_ai_stream

from tools.get_weather import get_weather
from tools.send_email import send_email
from tools.get_candidates import get_candidates
from tools.display_to_user import display_to_user
import time

tools=[get_weather, send_email, get_candidates, display_to_user]
async def send(message):
    print('🗯️ message', message)
    speak(message)
stream = create_ai_stream(websocket={"send": send }, tools=tools)

last_time = time.time()
start_time = last_time
#'S il ne neige pas demain à Rennes et qu il y a un plombier, envoi lui un email pour réparer mon toit.'
for chunk in stream('Affiches moi la météo à Rennes demain'):
    current_time = time.time()
    elapsed_time = current_time - last_time
    print('⏲️ elapsed_time', f'{elapsed_time:.4f} secondes', chunk["type"], chunk.get('message', ''))
    last_time = current_time

current_time = time.time()
elapsed_time = current_time - start_time
print('⏲️ elapsed_time', f'{elapsed_time:.4f} secondes')