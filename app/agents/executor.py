from abc import ABC
from typing import List, Dict, Any
import traceback
from core.tools import ToolState
import inspect

class ExecutorAgent(ABC): 
    def __init__(self, tools: List, state: ToolState):
        self.state = state     
        self.tools = tools

    def execute(self):
        current_step = self.state.get("current_step", 1) -1
        if not self.state.get("tools", []):
            self.state['steps'][current_step]['result'] = "Aucun outil à exécuter."
            self.state['steps'][current_step]['status'] = 'done'
            return self.state
        
        tools_to_execute = self.state["tools"]
        results = []

        for choice in tools_to_execute:
            result = self._execute_tool(choice, self.state['websocket'])
            results.append(result)

        # Formatage du résultat
        if results:
            self.state['steps'][current_step]['result'] = "\n".join(map(str, results))
            self.state['steps'][current_step]['status'] = 'done'
        else:
            self.state['steps'][current_step]['result'] = "Aucun résultat d'exécution."
            self.state['steps'][current_step]['status'] = 'done'

        # Nettoyage
        self.state["tools"] = []
        self.state["tool_exec"] = ""
        return self.state
        
    def _execute_tool(self, choice: Dict[str, Any], websocket) -> str:
        """Exécute un outil spécifique avec gestion d'erreurs améliorée"""
        if "function" not in choice:
            return f"⚠️ Erreur: 'function' manquant dans la définition de l'outil"
            
        tool_name = choice["function"]
        args = choice.get("args", {})
        tool = next((t for t in self.tools if t.name == tool_name), None)
        
        if not tool:
            return f"⚠️ Outil '{tool_name}' non trouvé"
            
        try:
            # Validation des arguments requis
            required_args = getattr(tool, "required_args", [])
            for arg in required_args:
                if arg not in args:
                    return f"⚠️ Argument requis '{arg}' manquant pour l'outil '{tool_name}'"
                    
            # Exécution de l'outil
            sig = inspect.signature(tool.func)
            params = sig.parameters
            if 'websocket' in params:
                result = tool.func(args, websocket=websocket)
            else:
                result = tool.func(args) 

            return f"✅ {tool_name}: {result}"
            
        except TypeError as e:
            error_details = str(e)
            return f"⚠️ Erreur de type dans '{tool_name}': {error_details}"
        except Exception as e:
            error_details = traceback.format_exc().splitlines()[-1]
            return f"⚠️ Erreur dans '{tool_name}': {error_details}"