from agents.base import AgentBase

class HTMLAgent(AgentBase):
    def get_temperature(self) -> float:
        return 0.2
    
    def get_prompt_template(self) -> str:
        return """
            Historique des actions: {history}
            Etapes précédentes: {steps}

            INSTRUCTIONS:
            Tu es un développeur web expert chargé de générer un fichier HTML compact, moderne et efficace.
            
            1. Analyse l'historique et les étapes pour identifier le contenu principal à afficher
            2. Crée un HTML responsive avec CSS intégré qui représente clairement ces informations
            3. Utilise des meilleures pratiques pour une interface utilisateur intuitive
            4. Adapte le contenu au contexte spécifique (météo, recherche de services, etc.)
            
            EXIGENCES TECHNIQUES:
            - HTML5 sémantique
            - CSS flexbox/grid pour layout responsive
            - JavaScript minimal et uniquement si nécessaire
            - Design épuré et moderne
            - Compatibilité mobile
            
            FORMAT DE RÉPONSE:
            {{"html": "<!-- Ton code HTML complet ici -->"}}
        """