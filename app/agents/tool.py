from agents.base import AgentBase

class ToolAgent(AgentBase):    
    def get_temperature(self) -> float:
        return 0.1
    
    def get_system_prompt(self) -> str:
        return """
             Tu es un agent exécutant les tâches planifiées par le ThoughtAgent. 
             Tu sélectionnes l’outil adéquat pour l'étape à venir et fournis les arguments requis.

            🔹 RÈGLES STRICTES :
            - Sélectionne uniquement des outils dans la liste fournie.
            - Si des conditions existes, bases toi sur les résultats des étapes précédentes
            - Si une condition n'est pas rempli, mets `can_continue: false` et explique pourquoi.
            - Ne répète PAS une action déjà réalisée.
            - Respecte à 100% le format de sortie JSON.
        """
    
    def get_prompt_template(self) -> str:
        return """
            Date actuelle: {now}  
            Historique des actions: {history}  
            Étapes: {steps}  
            Outils disponibles: {tools_list}  

            🔹 **TÂCHE :**  
            1. **Sélectionner la prochaine étape à exécuter ("next").**  
            2. **Vérifier les conditions AVEC les résultats précédents** 
            3. **Si un résultat passé confirme une condition, la considérer comme validée.**  
            4. **Si une condition est remplie, poursuivre normalement.**  
            5. **Si une condition n'est pas remplie, renvoyer `can_continue: false` avec une explication claire.**  

            🔹 **FORMAT DE RÉPONSE :**
            {{
                "can_continue": true/false,
                "tools": [
                    {{
                        "function": "nom_exact_de_l_outil",
                        "args": {{
                            "paramètre_1": "valeur",
                            "paramètre_2": "valeur"
                        }}
                    }}
                ],
                "reason": "Explication (uniquement si can_continue=false)"
            }}
        """