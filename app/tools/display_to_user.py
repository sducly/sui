from core.tools import ToolState
from langchain.tools import tool
import json
import asyncio
from agents.html import HTMLAgent

async def generate_html(design_prompt: str, websocket: object) -> str:
    initial_state = ToolState(
        history=design_prompt,
        use_tool=False,
        tool_exec="",
        tools_list=[],
        websocket=websocket
    )
    agent = HTMLAgent(state=initial_state) 
    html = agent.execute()
    await websocket.send(json.dumps({"type": "display_html", "html": html}))

@tool()
def display_to_user(design_prompt: str, websocket: object) -> str:
    """Génère et affiche du code HTML à l'utilisateur actuel via WebSocket.

    ⚠️ IMPORTANT : `design_prompt` doit être une **description textuelle** et non du HTML.

    Args:
        design_prompt (str): Un prompt décrivant le design souhaité et les informations nécessaires.
    
    Exemple de prompt à utiliser :
        - "Génére un module Météo avec la ville Rennes, météo Ensoleillé, code météo 3, température max 16.9°C, température min 10.5°C."
        - "Génére une carte affichant une liste de clients avec {nom: Thomas, prénom: Dupont}."

    Returns:
        str: Un message de confirmation indiquant que le code HTML a été envoyé à l'utilisateur.
    """
    asyncio.create_task(websocket.send(json.dumps({"type": "display_html", "html": """
        <style>
            .spinner {
                margin: 100px auto;
                width: 50px;
                height: 50px;
                border: 8px solid #f3f3f3;
                border-top: 8px solid #3498db;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
        <div class='spinner'></div>
    """})))

    asyncio.create_task(generate_html(design_prompt=design_prompt, websocket=websocket))
    return "Le code HTML sera affiché à l'utilisateur dans quelques secondes"
