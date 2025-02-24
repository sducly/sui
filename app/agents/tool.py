from agents.base import AgentBase

class ToolAgent(AgentBase):
    def get_prompt_template(self) -> str:
        return """
            Date courante: {now}
            Historique: {history}
            Outils disponibles: {tools_list}
            Sur la base de l'historique, choisis le prochain outil approprié et les arguments au format:
            {{"function": "<fonction>", "args": [<arg1>,<arg2>, ...]}}
            Respectes TOUJOURS le format défini pour les arguments
            N'inventes pas des arguments qui ne sont pas indiqués
        """