from .my_event import *
from .action import Action

class ActionMove(Action):
    
    def __init__(self, type, clicked_pos):
        self.type = type
        self.clicked_pos = clicked_pos


    def get_pos(self):
        return self.clicked_pos
        
    def get_type(self):
        return self.type