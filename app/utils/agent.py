from utils.tools import ToolState, clip_history, get_executor
from abc import ABC, abstractmethod
from langgraph.graph import StateGraph, END
from typing import Literal
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
        self.state["history"] = clip_history(self.state["history"])
        
        # Define the prompt template
        template = self.get_prompt_template()
        print(template)
        prompt = PromptTemplate.from_template(template)        
        llm = ChatOllama(model="lucie", format="json", temperature=0.1)
        llm_chain = prompt | llm | StrOutputParser()
        generation = llm_chain.invoke({
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
    
class ThoughtAgent(AgentBase):
    def get_prompt_template(self) -> str:
        return """
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

class ToolAgent(AgentBase):
    def get_prompt_template(self) -> str:
        return """
            Historique: {history}
            Outils disponibles: {tools_list}
            Sur la base de l'historique, choisis le prochain outil approprié et les arguments au format:
            {{"function": "<fonction>", "args": [<arg1>,<arg2>, ...]}}
            Respectes TOUJOURS le format défini pour les arguments
            N'inventes pas des arguments qui ne sont pas indiqués
        """
    
class AnimationAgent(AgentBase):
    def get_prompt_template(self) -> str:
        return """
            Historique: {history}
            Expressions faciales disponibles: 'smile', 'sad', 'funnyFace', 'surprise', 'angry', 'crazy'.
            Animations disponibles: 'Angry', 'Crying', 'Idle', 'Laughing', 'Rumba', 'Terrified'.
            Par défault, si aucune expression ne convient tu peux choisir Smile et Idle en animation.
            Sur la base de l'historique, choisis la prochaine expression faciale et l'animation qui convient:
            {{"facial_expression": "<expression_faciale_adaptée>", "animation": "<animation_adaptée>"}}
            N'inventes pas d'expressions faciales ou d'animations qui ne sont pas indiqués
        """

class FinalAgent(AgentBase):
    def get_prompt_template(self) -> str:
        return """
            Historique: {history}
            Tu es Lucie, une jeune femme qui travaille comme assistante virtuelle.
            Tu parles comme une personne réelle, avec un ton amical et naturel.
            Tu réponds aux questions de l'utilisateur de manière claire et concise, comme si tu étais une collègue ou une amie.
            Tu es toujours polie et gentille.
            Tu peux répondre à des questions personnelles ou non professionnelles.
            Réponds à la dernière question de l'utilisateur.
            - Produis le JSON au format: {{"final_answer": "ta réponse", "use_tool": false}}
        """
    
def agent_stream(tools=[]):
    def check_use_tool(state: ToolState) -> Literal["use tool", "not use tool"]:
        print(f"Valeur de use_tool: {state.get('use_tool')}")
        if state.get("use_tool") == True:
            print("check_use_tool: use tool")
            return "use tool"
        else:
            print("check_use_tool: not use tool")
            return "not use tool"

    workflow = StateGraph(ToolState)

    def thought_agent(state: ToolState) -> ToolState:
        return ThoughtAgent(state).execute()

    def tool_agent(state: ToolState) -> ToolState:
        return ToolAgent(state).execute()

    def final_agent(state: ToolState) -> ToolState:
        return FinalAgent(state).execute()
    
    def animation_agent(state: ToolState) -> ToolState:
        return AnimationAgent(state).execute()

    executor = get_executor(tools)
    workflow.add_node("animation_agent", animation_agent)
    workflow.add_node("thought_agent", thought_agent)
    workflow.add_node("tool_agent", tool_agent)
    workflow.add_node("tool", executor)
    workflow.add_node("final_agent", final_agent)

    workflow.set_entry_point("animation_agent")

    workflow.add_conditional_edges(
        "thought_agent",
        check_use_tool,
        {
            "use tool": "tool_agent",
            "not use tool": "final_agent",
        }
    )

    workflow.add_edge('tool_agent', 'tool')
    workflow.add_edge('animation_agent', 'thought_agent')

    workflow.add_edge('tool', 'thought_agent')
    workflow.add_edge('final_agent', END)

    tools_list = [tool.model_dump() for tool in tools]

    app = workflow.compile()

    now = datetime.now(timezone.utc).isoformat()
    initial_state = ToolState(
        history=f"Date courante :{now}",
        use_tool=False,
        tool_exec="",
        tools_list=tools_list
    )

    def stream(text: str):
        initial_state['history'] += f"\n{text}"
        for state in app.stream(initial_state):  # On récupère chaque chunk
            if 'thought_agent' in state:
                yield {
                    "type": "thought_agent",
                    "message": json.loads(state['thought_agent']['tool_exec']).get("scenario", "")
                }

            elif 'final_agent' in state:
                yield {
                    "type": "final_agent",
                    "message": json.loads(state['final_agent']['tool_exec']).get("final_answer", "")
                }

            elif 'tool_agent' in state:
                tool = json.loads(state['tool_agent']['tool_exec'])
                yield {
                    "type": "tool_agent",
                    "function": tool.get("function", ""),
                    "args": tool.get("args", "")
                }
            elif 'animation_agent' in state:
                tool = json.loads(state['animation_agent']['tool_exec'])
                yield {
                    "type": "animation_agent",
                    "facial_expression": tool.get("facial_expression", ""),
                    "animation": tool.get("animation", "")
                }
    
    return stream