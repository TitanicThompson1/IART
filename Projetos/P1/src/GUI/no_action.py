from .my_event import *
from .action import Action


class NoAction(Action):

    def __init__(self):
        pass

    def get_type(self):
        return MyEvent.NOEVENT