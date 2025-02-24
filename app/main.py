import asyncio
import websockets 
import json

from core.tts import speak
from core.ai_stream import create_ai_stream

from tools.get_weather import get_weather
from tools.send_email import send_email
from tools.get_candidates import get_candidates

tools=[get_weather, send_email, get_candidates]

async def main(websocket):
    stream = create_ai_stream(websocket=websocket, tools=tools)
    while True:
        try:
            message = await websocket.recv()
            print(f"📨 Message reçu du client: {message}")
            
            for chunk in stream(message):
                match chunk["type"]:
                    case "thought_agent":
                        action_data = {
                            "type": "thought",
                            "message": chunk['message']
                        }
                        await websocket.send(json.dumps(action_data))
                    case "final_agent":
                        audio_data = await speak(chunk['message'])
                        data = {
                            "type": "audio",
                            "message": chunk['message'],
                            "audio": audio_data["audio"],
                            "animation": "Idle",
                            "facialExpression": "smile",
                            "lipsync": audio_data["phonemes"]
                        }
                        await websocket.send(json.dumps(data))
                    case "tool_agent":
                        action_data = {
                            "type": "tool",
                            "tool":chunk['function'],
                            "tool_input": chunk['args'],
                        }
                        await websocket.send(json.dumps(action_data)) 
                    case "iterate_agent":
                        action_data = {
                            "type": "steps",
                            "steps":chunk['steps'],
                        }
                        await websocket.send(json.dumps(action_data)) 

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