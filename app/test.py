from utils.agent import agent_stream
from app.tools.get_weather import get_weather
import json

tools = [get_weather]

stream = agent_stream(tools)

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    
    for chunk in stream(user_input):
        match chunk["type"]:
            case "chat_agent":
                print(f"Chat: {chunk['message']}")
            case "final_agent":
                print(f"Final: {chunk['message']}")
            case "tool_agent":
                print(f"Tool: {chunk['function']} avec args {chunk['args']}")