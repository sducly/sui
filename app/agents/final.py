from agents.base import AgentBase
from core.tools import clip_history
import json

class FinalAgent(AgentBase):
    def get_temperature(self) -> float:
        return 0.4
    
    def get_system_prompt(self) -> str:
        return """ 
            Tu es un assistant intelligent qui résume brièvement les résultats et répond directement à l'utilisateur. 

            🔹 RÈGLES STRICTES :
            - Réponse ULTRA concise (2-3 phrases max).
            - Format texte brut uniquement.
            - Pas de questions à l'utilisateur.
            - Pas d'emoji, HTML ou Markdown.
        """
    
    def get_prompt_template(self) -> str:
        return """
            Date: {now}
            Utilisateur: {user}
            Étapes exécutées: {steps}
            Historique: {history}

            🔹 INSTRUCTIONS :
            1. Résume en une phrase ce qui a été accompli.
            2. Réponds DIRECTEMENT à la dernière demande de l'utilisateur.
            3. Sois bref, naturel et précis.

            🔹 FORMAT DE RÉPONSE :
            {{
                "final_answer": "Réponse concise ici."
            }}
        """
    
    def execute(self):
        state = super().execute()
        message = json.loads(self.state['tool_exec']).get("final_answer", "")
        self.state["history"] += "\n" + message
        return state