from agents.base import AgentBase

class AnimationAgent(AgentBase):
    def get_temperature(self) -> float:
        return 0.7
    
    def get_prompt_template(self) -> str:
        return """
                Date courante: {now}
                Historique: {history}
                
                EXPRESSIONS FACIALES DISPONIBLES:
                - 'smile' (sourire - pour situations positives/neutres)
                - 'sad' (triste - pour mauvaises nouvelles/sympathie)
                - 'funnyFace' (amusé - pour humour/légèreté)
                - 'surprise' (surpris - pour étonnement/nouveauté)
                - 'angry' (en colère - pour frustration/problèmes)
                - 'crazy' (fou - pour idées excentriques/enthousiastes)
                
                ANIMATIONS DISPONIBLES:
                - 'Idle' (neutre - position par défaut)
                - 'Sad' (triste - pour émotions négatives)
                
                TÂCHE:
                Analyse la dernière interaction dans l'historique et sélectionne l'expression faciale et l'animation les plus appropriées.
                
                FORMAT DE RÉPONSE (JSON strict):
                {{"facial_expression": "expression_choisie", "animation": "animation_choisie"}}
            """