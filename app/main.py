import asyncio
import websockets 
import json

from outputs.speech import speak
from utils.agent import agent_stream
from tools.get_weather import get_weather
from tools.send_email import send_email
from tools.get_candidates import get_candidates
import random 

tools=[get_weather, send_email, get_candidates]
stream = agent_stream(tools)

async def main(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(f"Message reçu du client: {message}")
            
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
                            "animation": random.choice(["Talking_0", "Talking_1", "Talking_2"]),
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
                    case "animation_agent":
                        action_data = {
                            "type": "animation",
                            "facialExpression":chunk['facial_expression'],
                            "animation": chunk['animation'],
                            "audio": "",
                            "lipsync": ""
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