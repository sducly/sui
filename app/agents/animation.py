from agents.base import AgentBase

class AnimationAgent(AgentBase):
    def get_model(self) -> str:
        return "phi4-mini"
    
    def get_prompt_template(self) -> str:
        return """
            Date courante: {now}
            Historique: {history}
            Expressions faciales disponibles: 'smile', 'sad', 'funnyFace', 'surprise', 'angry', 'crazy'.
            Animations disponibles: 'Idle', 'Sad'.
            Par défault, si aucune expression ne convient tu peux choisir Smile et Idle en animation.
            Sur la base de l'historique, choisis la prochaine expression faciale et l'animation qui convient:
            {{"facial_expression": "<expression_faciale_adaptée>", "animation": "<animation_adaptée>"}}
            N'inventes pas d'expressions faciales ou d'animations qui ne sont pas indiqués
        """