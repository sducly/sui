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

    def execute(self) -> ToolState:
        now = datetime.now(timezone.utc).isoformat()
        self.state["history"] = clip_history(self.state["history"])
        template = self.get_prompt_template()
        prompt = PromptTemplate.from_template(template)        
        llm = ChatOllama(model="phi4", format="json", temperature=0.1)
        llm_chain = prompt | llm | StrOutputParser()
        generation = llm_chain.invoke({
            "now": now,
            "history": self.state["history"], 
            "use_tool": self.state["use_tool"],
            "tools_list": self.state["tools_list"]
        })
        data = json.loads(generation)
        self.state["use_tool"] = data.get("use_tool", False)        
        self.state["tool_exec"] = generation

        self.state["history"] += "\n" + generation
        self.state["history"] = clip_history(self.state["history"])

        return self.state