import asyncio
import websockets
import json
import threading
from inputs.speech import listen
from inputs.vision import detect_face
from state import State
from ollama import chat
from datetime import datetime, timezone
from utils.tools import function_to_dict
from tools.add_reminder import add_reminder
from tools.get_weather import get_weather
import re
from outputs.speech import speak

state = State()

available_functions = {
    "get_weather": function_to_dict(get_weather),
    "add_reminder": function_to_dict(add_reminder)
}

json_functions = json.dumps(list(available_functions.keys()))

def execute_functions(function_calls):
    function_results = {}
    executed_functions = []

    for function_call in function_calls:
        function_name = function_call.get('function')
        params = function_call.get('params', {})

        if function_name not in available_functions:
            print(f"⚠️ Fonction inconnue : {function_name}")
            continue

        function_meta = available_functions[function_name]
        required_params = function_meta.get("parameters", {}).keys()

        for param, value in params.items():
            if isinstance(value, str) and value.startswith("response."):
                key = value.split(".")[1]
                params[param] = function_results.get(key, None)

        missing_params = [p for p in required_params if p not in params]
        if missing_params:
            print(f"⚠️ Paramètres manquants pour {function_name}: {missing_params}")
            continue

        try:
            function_result = globals()[function_name](**params)
            function_results[function_name] = function_result
            executed_functions.append({function_name: function_result})
        except Exception as e:
            print(f"⚠️ Erreur lors de l'exécution de {function_name}: {e}")

    return executed_functions

class SentenceBuffer:
    def __init__(self):
        self.buffer = ""
        self.sentence_endings = {'.', '?', '!', '\n'}
    
    def add_text(self, text):
        self.buffer += text
        sentences = []
        
        while True:
            sentence_end = -1
            for ending in self.sentence_endings:
                pos = self.buffer.find(ending)
                if pos != -1 and (sentence_end == -1 or pos < sentence_end):
                    sentence_end = pos
            
            if sentence_end == -1:
                break
                
            sentence = self.buffer[:sentence_end + 1].strip()
            if sentence:
                sentences.append(sentence)
            
            self.buffer = self.buffer[sentence_end + 1:]
        
        return sentences

async def process_stream_with_sentences(stream, websocket):
    sentence_buffer = SentenceBuffer()
    
    for chunk in stream:
        if 'message' in chunk and 'content' in chunk['message']:
            content = chunk['message']['content']
            
            sentences = sentence_buffer.add_text(content)
            for sentence in sentences:
                if sentence.strip():
                    try:
                        audio_data = await speak(sentence)
                        data = {
                            "audio": audio_data["audio"],
                            "animation": 'Idle',
                            "facialExpression": "smile",
                            "lipsync": audio_data["phonemes"]
                        }
                        await websocket.send(json.dumps(data))
                    except Exception as e:
                        print(f"Erreur lors de l'envoi de la phrase: {e}")
    
    remaining = sentence_buffer.buffer.strip()
    if remaining:
        try:
            audio_data = await speak(remaining)
            data = {
                "audio": audio_data["audio"],
                "animation": 'Idle',
                "facialExpression": "smile",
                "lipsync": audio_data["phonemes"]
            }
            await websocket.send(json.dumps(data))
        except Exception as e:
            print(f"Erreur lors de l'envoi du reste du buffer: {e}")

async def get_function_response(message):
    response = chat(
        model='functions',
        messages=[
            {'role': 'user', 'content': message},
            {'role': 'user', 'content': f"Return ONLY a valid JSON array with the function calls:{json_functions}"}
        ]
    )
    return response['message']['content']

async def main(websocket):
    threading.Thread(target=detect_face, args=(state.update_vision,), daemon=True).start()
    threading.Thread(target=listen, args=(state.update_audio,), daemon=True).start()

    while True:
        try:
            raw_message = await websocket.recv()
            print(f"Message reçu du client: {raw_message}")

            now = datetime.now(timezone.utc).isoformat()
            message = f"{raw_message} \n\n(ACTUAL_DATETIME: {now})"

            # Premier appel sans streaming pour les function calls
            function_response = await get_function_response(message)

            try:
                match = re.search(r'```json\n(.*)\n```', function_response, flags=re.DOTALL)
                function_calls_json = match.group(1) if match else function_response

                function_calls = json.loads(function_calls_json)
                if not isinstance(function_calls, list):
                    function_calls = []

                function_results = execute_functions(function_calls)
                function_result = json.dumps(function_results)

                # Deuxième appel avec streaming pour la réponse finale
                response_stream = chat(
                    model='sui',
                    messages=[
                        {'role': 'user', 'content': message},
                        {'role': 'assistant', 'content': function_result}
                    ],
                    stream=True
                )

                await process_stream_with_sentences(response_stream, websocket)

            except Exception as e:
                print(f"Une erreur est survenue : {e}")
                await websocket.send(json.dumps({"speech": str(e), "face": state.vision}))

        except websockets.exceptions.ConnectionClosedOK:
            print("Client disconnected.")
            break
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            break

async def run():
    server = await websockets.serve(main, "0.0.0.0", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(run())