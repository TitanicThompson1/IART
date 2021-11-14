from .my_event import *
from .action import Action

from enum import Enum

class AI(Enum):
    BFS = 0
    UCS = 1
    DFS = 2
    IDS = 3
    GREEDY = 4
    ASTAR = 5


class ActionAI(Action):
    
    def __init__(self, ai_type):
        super().__init__(MyEvent.AI)
        self.ai_type = ai_type


    def get_ai_type(self):
        return self.ai_type
    

    