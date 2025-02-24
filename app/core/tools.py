from typing import TypedDict, List
import json

def clip_history(history: str, max_chars: int = 8000) -> str:
    if len(history) > max_chars:
        return history[-max_chars:]
    return history

class ToolState(TypedDict):
    history: str
    use_tool: bool
    tool_exec: str
    tools_list: str

def get_executor(tools: List):
    def ToolExecutor(state: ToolState) -> ToolState:
        if not state["tool_exec"]:
            raise ValueError("No tool_exec data available to execute.")
        choice = json.loads(state["tool_exec"])

        if "function" not in choice:
            state["history"] += f"\nToolExecutor: 'function' manquant dans {state['tool_exec']}"
            state["use_tool"] = False
            state["tool_exec"] = ""
            return state
        
        tool_name = choice["function"]
        args = choice["args"]
        
        tool = next((t for t in tools if t.name == tool_name), None)

        if not tool:
            state["history"] += f"\nTool {tool_name} not found."
            state["use_tool"] = False
            state["tool_exec"] = ""
            return state
        
        result = tool.func(*args)
        state["history"] += f"\nExecuted {tool_name} with result: {result}"
        state["history"] = clip_history(state["history"])
        state["use_tool"] = False
        state["tool_exec"] = ""
        return state
    
    return ToolExecutor