from agents.base import AgentBase

class ThoughtAgent(AgentBase):
    def get_temperature(self) -> int:
        return 0.5

    def get_prompt_template(self) -> str:
        return """
            Date courante: {now}
            Outils disponibles: {tools_list}
            Historique: {history}
            En tant que ThoughtAgent, analyse la DERNIERE phrase de l'historique.
            Si la DERNIERE phrase demande d'utiliser un outils, alors utilise un outil.
            Si la DERNIERE phrase est une question personnelle, ou si aucun outil n'est nécessaire ou si toutes les conditions sont remplies, fournis une réponse finale.
            Tes réponses doivent être courtes et concises. 
            Produis le JSON au format: {{"scenario": "ta réponse", "use_tool": true/false}}.
            Exemple si un outil doit être appelé : {{"scenario": "J'appelle l'outil get_weather", "use_tool": true}}
            Exemple si aucun outil n'est nécessaire : {{"scenario": "Je n'ai pas besoin d'appeler d'outil", "use_tool": false}}
        """