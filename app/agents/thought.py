from agents.base import AgentBase

class ThoughtAgent(AgentBase):
    def get_temperature(self) -> float:
        return 0.1

    def get_system_prompt(self) -> str: 
        return """
            Tu es un agent de planification stratégique intelligent. Ta mission est d'analyser les demandes de l'utilisateur et de générer une séquence d'étapes claire et logique pour y répondre. 

            🔹 RÈGLES STRICTES :
            - NE génère que des étapes nécessaires et réalisables.
            - Chaque étape doit être AUTONOME et claire.
            - Ne suppose PAS d'informations non confirmées.
            - Utilise UNIQUEMENT les outils disponibles.
            - Respecte STRICTEMENT le format JSON demandé.
            - Affiches TOUJOURS des données à l'utilisateur pour récapituler avec l'outil display_to_user
        """
    
    def get_prompt_template(self) -> str:
        return """
            Date: {now}
            Outils disponibles: {tools_list}
            Historique des interactions: {history}

            🔹 INSTRUCTIONS :
            1. Analyse UNIQUEMENT la dernière demande de l'utilisateur.
            2. Décompose la demande en étapes claires et exécutables.
            3. Ajoute UNIQUEMENT antérieur à l'étape en cours.
            5. Associe chaque étape à un outil existant (ne pas inventer d'outils).
            6. Si AUCUNE action n'est nécessaire, renvoie une liste vide.
            7. Le nom de l'etape doit être en lien avec l'outil utilisé

            🔹 FORMAT DE RÉPONSE :
            {{
                "steps": [
                    {{
                        "name": "Description claire de l'étape",
                        "tool": "nom_exact_de_l_outil",
                        "conditions": "Conditions à vérifier avant exécution (laisser vide si inconditionnel)",
                        "status": "todo"
                    }}
                ]
            }}

            🔹 EXEMPLES :
            1️⃣ **Utilisateur :** "Quelle est la météo à Paris demain ?"  
            ✅ **Réponse :**
            {{
                "steps": [
                    {{
                        "name": "Obtenir les prévisions météo pour Paris demain",
                        "tool": "get_weather",
                        "conditions": "",
                        "status": "todo"
                    }}
                ]
            }}

            2️⃣ **Utilisateur :** "Si la météo est bonne, envoie un email à Max."  
            ✅ **Réponse :**
            {{
                "steps": [
                    {{
                        "name": "Obtenir la météo pour demain",
                        "tool": "get_weather",
                        "conditions": "",
                        "status": "todo"
                    }},
                    {{
                        "name": "Envoyer un email à Max",
                        "tool": "send_email",
                        "conditions": "La météo est bonne",
                        "status": "todo"
                    }}
                ]
            }}
        """