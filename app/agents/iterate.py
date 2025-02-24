from agents.base import AgentBase
from core.tools import ToolState
from abc import ABC

class IterateAgent(ABC): 
    def __init__(self, state: ToolState):
        self.state = state   

    def execute(self):
        steps = self.state.get("steps", [])
        current_step = self.state.get("current_step", 0)

        if self.state.get("can_continue") == False:

            current_step = self.state.get("current_step", 1) - 1
            steps = self.state.get("steps", [])
            
            for step in steps[current_step:]:
                step["status"] = "canceled"
            
            self.state['next_agent'] = 'final_agent'
            return self.state

        if not steps:
            self.state['next_agent'] = 'final_agent'
            return self.state

        if not steps or current_step >= len(steps):
            self.state['steps'][current_step - 1]['status'] = 'done'
            self.state['next_agent'] = 'final_agent'
            return self.state
        
        self.state["current_step"] += 1 

        self.state['steps'][current_step]['status'] = 'next'

        if current_step > 0:
            self.state['steps'][current_step - 1]['status'] = 'done'


        self.state['next_agent'] = 'tool_agent'
        return self.state