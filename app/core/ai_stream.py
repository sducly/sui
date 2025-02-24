from langgraph.graph import StateGraph, END
from typing import Literal
import json

from agents.thought import ThoughtAgent
from agents.animation import AnimationAgent
from agents.final import FinalAgent
from agents.tool import ToolAgent
from agents.display import DisplayAgent
from core.tools import ToolState, get_executor

def create_ai_stream(tools=[]):
    def check_use_tool(state: ToolState) -> Literal["use tool", "not use tool"]:
        print(f"Valeur de use_tool: {state.get('use_tool')}")
        if state.get("use_tool") == True:
            return "use tool"
        else:
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
    
    def display_agent(state: ToolState) -> ToolState:
        return DisplayAgent(state).execute()

    executor = get_executor(tools)
    workflow.add_node("animation_agent", animation_agent)
    workflow.add_node("thought_agent", thought_agent)
    workflow.add_node("tool_agent", tool_agent)
    workflow.add_node("display_agent", display_agent)
    workflow.add_node("tool", executor)
    workflow.add_node("final_agent", final_agent)

    workflow.set_entry_point("animation_agent")

    workflow.add_edge('animation_agent', 'thought_agent')

    workflow.add_conditional_edges(
        "thought_agent",
        check_use_tool,
        {
            "use tool": "tool_agent",
            "not use tool": "display_agent",
        }
    )

    workflow.add_edge('tool_agent', 'tool')


    workflow.add_edge('tool', 'thought_agent')
    workflow.add_edge('display_agent', 'final_agent') 
    workflow.add_edge('final_agent', END)

    tools_list = [tool.model_dump() for tool in tools]

    app = workflow.compile()

    initial_state = ToolState(
        history="",
        use_tool=False,
        tool_exec="",
        tools_list=tools_list,
    )

    def stream(text: str):
        initial_state['history'] += f"\n{text}"
        for state in app.stream(initial_state):  
            if 'thought_agent' in state:
                yield {
                    "type": "thought_agent",
                    "message": json.loads(state['thought_agent']['tool_exec']).get("scenario", "")
                }
            if 'display_agent' in state:
                yield {
                    "type": "display_agent",
                    "message": json.loads(state['display_agent']['tool_exec']).get("html", "")
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