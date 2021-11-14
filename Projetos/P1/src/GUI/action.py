from .my_event import *


class Action:

    def __init__(self, type):
        self.type = type
        pass

    def get_type(self):
        return self.type
    
