from core.tools import ToolState, clip_history
from abc import ABC, abstractmethod
import json
from langchain_ollama.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from abc import ABC, abstractmethod
from datetime import datetime, timezone

class AgentBase(ABC):
    def __init__(self, state: ToolState):
        self.state = state

    @abstractmethod
    def get_prompt_template(self) -> str:
        pass

    def get_model(self) -> str:
        return "phi4"

    def get_temperature(self) -> float:
        return 0.1
        
    def get_system_prompt(self) -> str:
        return "Tu es un agent intelligent qui analyse les informations et répond de façon précise et concise au format JSON."

    def execute(self) -> ToolState:
        now = datetime.now(timezone.utc).isoformat()
        self.state["history"] = clip_history(self.state["history"])
        template = self.get_prompt_template()
        prompt = PromptTemplate.from_template(template)
        llm = ChatOllama(
            model=self.get_model(),
            format="json",
            temperature=self.get_temperature(),
            system=self.get_system_prompt() 
        )
        llm_chain = prompt | llm | StrOutputParser()

        generation = llm_chain.invoke({
            "now": now,
            "history": self.state["history"],
            "tools_list": self.state.get("tools_list", []),
            "steps": self.state.get('steps', []),
            "user": {"first_name": "Sébastien", "lastname": "DUCLY", "email": "sebastien.ducly@gmail.com"}
        })

        try:
            data = json.loads(generation)
            if(data.get("reason", False)):
                self.state["history"] += "\n" + data.get("reason", "")

            self.state['steps'] = [
                step for step in data.get("steps", self.state.get('steps', []))
                if step.get('tool')  
            ]
            self.state["tools"] = data.get("tools", [])
            self.state["can_continue"] = data.get("can_continue", True)
           
            self.state["tool_exec"] = generation
        except json.JSONDecodeError:
            self.state["history"] += "\nErreur: Réponse non JSON"
            self.state["tool_exec"] = json.dumps({"error": "Format JSON invalide", "raw": generation})
            self.state["can_continue"] = False
            
        return self.state