import requests
import json
import re
from fastapi import Body, FastAPI
from tools.reminder import add_reminder
from pydantic import BaseModel
from datetime import datetime, timezone

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """Interagit avec Ollama et exécute les tools si besoin"""

    now = datetime.now(timezone.utc).isoformat()

    # 🔥 Ajouter l'heure actuelle dans le prompt
    full_prompt = f"{request.prompt}\n\n(ACTUAL_DATETIME: {now})"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "sui", "prompt": full_prompt, "stream": False}
    )
    
    text = response.json()["response"]
    print("Réponse brute :", text)

    # 🔍 Extraction du JSON dans la réponse
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        json_part = match.group(1)
        try:
            data = json.loads(json_part)
            if data.get("function") == "set_reminder":
                message = data["params"]["task"]
                datetime_str = data["params"]["date"]
                print("Ajout du rappel :", message, datetime_str)
                add_reminder(message, datetime_str)
                response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "sui", "prompt": f"Sui note le rappel : {message}. Dis-le avec ton style !", "stream": False}
            ).json()["response"]
                return {"response": response}
        except json.JSONDecodeError:
            print("Erreur : JSON mal formé")

    return {"response": text}
