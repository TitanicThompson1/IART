
from ai import *
from file_reader import *
from GUI import *
from controller import *


controller = Controller()

gui = Gui(controller.get_puzzle())


# Gets the desired action of the user
action = gui.get_action()

while action.get_type() != MyEvent.QUIT:

    # Processes the action
    controller.process_action(action)
    
    # Displays the current state of the game
    gui.display()

    # Gets next action
    action = gui.get_action()

gui.close()
