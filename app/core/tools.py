from typing import TypedDict               

def clip_history(history: str, max_chars: int = 4096) -> str:
    if len(history) > max_chars:
        return history[-max_chars:]
    return history

class ToolState(TypedDict):
    history: str
    tools: list
    tool_exec: str
    tools_list: str
    websocket: object
    steps: str
    current_step: int
    can_continue: bool
    next_agent: str