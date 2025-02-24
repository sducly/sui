from langgraph.graph import StateGraph, END
from typing import Literal, Dict, Any
import json
import asyncio
import logging
from datetime import datetime
from langchain_ollama.chat_models import ChatOllama

from agents.thought import ThoughtAgent
from agents.final import FinalAgent
from agents.tool import ToolAgent
from agents.html import HTMLAgent
from agents.iterate import IterateAgent
from agents.executor import ExecutorAgent
from agents.animation import AnimationAgent
from core.tools import ToolState

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ai_stream")

def create_ai_stream(websocket, tools=[]):
    """
    Crée un flux d'exécution d'agents IA avec un graphe d'états.
    
    Args:
        websocket: Le websocket pour la communication temps réel
        tools: Liste des outils disponibles pour les agents
        
    Returns:
        Une fonction stream qui génère les différentes étapes d'exécution
    """
    def use_tool(state: ToolState) -> Literal["tool", 'no_tool', 'break']:
        """Détermine si des outils doivent être utilisés"""
        if state.get("can_continue") == False:
            return "break"
        return "tool" if len(state.get("tools", [])) > 0 else "no_tool"
    
    def use_agent(state: ToolState) -> str:
        """Détermine le prochain agent à utiliser"""
        return state.get("next_agent", "final_agent")
    
        # Préparation des outils disponibles
    tools_list = [tool.model_dump() for tool in tools]

    # État initial
    initial_state = ToolState(
        history="",
        tools=[],
        tool_exec="",
        tools_list=tools_list,
        websocket=websocket,
        steps=[],
        current_step=0,
        can_continue=True,
        execution_start=datetime.now().isoformat(),
    )

    ThoughtAgent(initial_state).execute()

    # Création du graphe d'états
    workflow = StateGraph(ToolState)
    
    # Définition des fonctions d'exécution des agents
    def thought_agent(state: ToolState) -> ToolState:
       result =  ThoughtAgent(state).execute()
       print('🗯️ thought agent', result['tool_exec'])
       return result

    def animation_agent(state: ToolState) -> ToolState:
        return AnimationAgent(state).execute()
    
    def executor_agent(state: ToolState) -> ToolState:
        return ExecutorAgent(state=state, tools=tools).execute()
    
    def iterate_agent(state: ToolState) -> ToolState:
        return IterateAgent(state).execute()

    def final_agent(state: ToolState) -> ToolState:
       response = FinalAgent(state).execute()
       print(response['tool_exec'])
       return response
    
    def tool_agent(state: ToolState) -> ToolState:
        print('🥩 steps ', state['steps'])
        result =  ToolAgent(state).execute()
        print('☠️ tool agent', state['tool_exec'])
        return result
    
    # Ajout des nœuds au graphe
    workflow.add_node("thought_agent", thought_agent)
    workflow.add_node("animation_agent", animation_agent)
    workflow.add_node("executor_agent", executor_agent)
    workflow.add_node("final_agent", final_agent)
    workflow.add_node("tool_agent", tool_agent)
    workflow.add_node("iterate_agent", iterate_agent)

    # Définition du point d'entrée
    workflow.set_entry_point("thought_agent")

    # Définition des transitions directes
    workflow.add_edge("thought_agent", "animation_agent")
    workflow.add_edge("animation_agent", "iterate_agent")
    workflow.add_edge("executor_agent", "iterate_agent")

    # Définition des transitions conditionnelles
    workflow.add_conditional_edges(
        "iterate_agent",
        use_agent,
        {
            "tool_agent": "tool_agent",
            "final_agent": "final_agent"
        }
    )   

    workflow.add_conditional_edges(
        "tool_agent",
        use_tool,
        {
            "tool": "executor_agent",
            "no_tool": "iterate_agent",
            "break": "final_agent"
        }
    )

    # Définition de la sortie
    workflow.add_edge("final_agent", END)

    # Compilation du graphe
    app = workflow.compile()

    def stream(text: str):
        """
        Génère un flux d'événements à partir de l'exécution du graphe d'agents.
        
        Args:
            text: Le texte de la requête utilisateur
            
        Yields:
            Dictionnaires contenant les informations de chaque étape d'exécution
        """
        # Ajout du texte à l'historique
        initial_state['history'] += f"{text}"
        execution_id = datetime.now().strftime("%Y%m%d%H%M%S")
        logger.info(f"Démarrage de l'exécution {execution_id} avec le message: {text[:50]}...")

        # Streaming des résultats
        for state in app.stream(initial_state):
            try:
                # Traitement pour l'agent de pensée
                if 'thought_agent' in state:
                    thought_data = state['thought_agent']
                    steps = thought_data.get("steps", [])
                    initial_state['steps'] = steps
                    message = _safe_json_dumps(steps)
                    yield {
                        "type": "thought_agent",
                        "message": message,
                        "timestamp": datetime.now().isoformat()
                    }
                
                # Traitement pour l'agent d'animation
                elif 'animation_agent' in state:
                    animation_data = state['animation_agent']
                    try:
                        animation = json.loads(animation_data['tool_exec'])
                        yield {
                            "type": "animation_agent",
                            "facial_expression": animation.get("facial_expression", "smile"),
                            "animation": animation.get("animation", "Idle"),
                            "timestamp": datetime.now().isoformat()
                        }
                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error(f"Erreur dans animation_agent: {e}")
                        yield {
                            "type": "animation_agent",
                            "facial_expression": "smile",
                            "animation": "Idle",
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        }
                
                # Traitement pour l'agent HTML
                elif 'final_agent' in state:
                    html_data = state['final_agent']
                    try:
                        message = json.loads(html_data['tool_exec']).get("html", "")
                        yield {
                            "type": "final_agent",
                            "message": message,
                            "timestamp": datetime.now().isoformat()
                        }
                    except json.JSONDecodeError as e:
                        logger.error(f"Erreur de décodage JSON dans final_agent: {e}")
                        yield {
                            "type": "final_agent",
                            "message": "<p>Erreur de génération HTML</p>",
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        }
                
                # Traitement pour l'agent final
                elif 'final_agent' in state:
                    final_data = state['final_agent']
                    try:
                        message = json.loads(final_data['tool_exec']).get("final_answer", "")
                        yield {
                            "type": "final_agent",
                            "message": message,
                            "timestamp": datetime.now().isoformat()
                        }
                    except json.JSONDecodeError as e:
                        logger.error(f"Erreur de décodage JSON dans final_agent: {e}")
                        yield {
                            "type": "final_agent",
                            "message": "Je n'ai pas pu générer une réponse appropriée.",
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        }
                
                # Traitement pour l'agent d'outils
                elif 'tool_agent' in state:
                    tool_data = state['tool_agent']
                    try:
                        tool = json.loads(tool_data['tool_exec'])
                        function = tool.get("function", "")
                        args = tool.get("args", "")
                        yield {
                            "type": "tool_agent",
                            "function": function,
                            "args": args,
                            "timestamp": datetime.now().isoformat()
                        }
                    except json.JSONDecodeError as e:
                        logger.error(f"Erreur de décodage JSON dans tool_agent: {e}")
                        yield {
                            "type": "tool_agent",
                            "function": "",
                            "args": "",
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        }
                
                # Traitement pour l'agent d'itération
                elif 'iterate_agent' in state:
                    iterate_data = state['iterate_agent']
                    steps = iterate_data.get('steps', [])
                    yield {
                        "type": "iterate_agent",
                        "steps": _safe_json_dumps(steps),
                        "current_step": iterate_data.get('current_step', 0),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                # Traitement pour l'agent d'exécution
                elif 'executor_agent' in state:
                    executor_data = state['executor_agent']
                    current_step = executor_data.get('current_step', 0) - 1
                    if current_step >= 0 and current_step < len(executor_data.get('steps', [])):
                        result = executor_data['steps'][current_step].get('result', "")
                        yield {
                            "type": "executor_agent",
                            "result": result,
                            "step": current_step,
                            "timestamp": datetime.now().isoformat()
                        }
                
            except Exception as e:
                logger.error(f"Erreur dans le traitement d'état: {e}")
                yield {
                    "type": "error",
                    "message": f"Une erreur s'est produite: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }

        logger.info(f"Fin de l'exécution {execution_id}")

    def _safe_json_dumps(obj: Any) -> str:
        """Convertit un objet en JSON avec gestion d'erreur"""
        try:
            return json.dumps(obj, indent=2, ensure_ascii=False)
        except (TypeError, OverflowError) as e:
            logger.error(f"Erreur lors de la sérialisation JSON: {e}")
            return json.dumps({"error": "Impossible de sérialiser l'objet"})

    return stream