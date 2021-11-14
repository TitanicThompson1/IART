from GUI import *
from data import *
from ai import *
import time
from file_reader import *

#if CHECK_TIME = 0, then not wanted to print elapsed time
CHECK_TIME = 1

import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../puzzles/puz6x6facil.pzl"
abs_file_path = os.path.join(script_dir, rel_path)


class Controller:
    """This classs controls the puzzle. It processes the actions of the user and changes the puzzle accordingly
    """
    def __init__(self):
        
        # All the avaiable puzzles for the user
        self.all_puzzles = ['../puzzles/test_puzzle.pzl', '../puzzles/test_puzzle2.pzl', '../puzzles/puz6x6facil.pzl', '../puzzles/puz6x6facil_2.pzl', '../puzzles/puz6x6medio.pzl',
                            '../puzzles/puz6x6dificil.pzl', 
                            '../puzzles/puz10x10facil.pzl', '../puzzles/puz10x10medio.pzl', '../puzzles/puz10x10dificil.pzl',
                            '../puzzles/puz10h.pzl'
                            ]

        # The indice of the current puzzle
        self.current_pzl = 0

        # The current puzzle
        self.puzzle = read_puzzle(os.path.join(script_dir, self.all_puzzles[self.current_pzl]))


    def get_puzzle(self):
        return self.puzzle


    def process_action(self, action):
        """ Processes the action and changes the puzzle accordingly
        """

     
        # Fill an aquarium
        if action.get_type() == MyEvent.FILL and not self.puzzle.is_done():
            self._fill_level(action.get_pos())

        # Empty an aquarium
        elif action.get_type() == MyEvent.EMPTY and not self.puzzle.is_done():
            self._empty_level(action.get_pos())

        # Reset the puzzle
        elif action.get_type() == MyEvent.RESET:
            self._reset()
        
        # Checks if the current puzzle is the solution
        elif action.get_type() == MyEvent.CHCK_SOL:
            self._check_solution()
        
        # Starts the AI
        elif action.get_type() == MyEvent.AI and not self.puzzle.is_done():
            self._algorithm(action.get_ai_type())

        # Loads the next puzzle in the list
        elif action.get_type() == MyEvent.N_PZL:
            self._next_puzzle()

        # Loads the previous puzzle in the list
        elif action.get_type() == MyEvent.P_PZL:
            self._previous_puzzle()


    def _previous_puzzle(self):
        """Changes the puzzle to the previous one of the list. If the current puzzle is the first,
        then does nothing
        """
        if self.current_pzl > 0:
            self.current_pzl -= 1
            new_puzzle = read_puzzle(os.path.join(script_dir, self.all_puzzles[self.current_pzl]))
            self.puzzle.transform_into(new_puzzle)


    def _next_puzzle(self):
        """Changes the puzzle to the next one of the list. If the current puzzle is the last,
        then does nothing
        """
        if self.current_pzl < len(self.all_puzzles) - 1:
            self.current_pzl += 1
            new_puzzle = read_puzzle(os.path.join(script_dir, self.all_puzzles[self.current_pzl]))
            self.puzzle.transform_into(new_puzzle)

    
            
            
    def _fill_level(self, pos):
        """Fills a level of the aquarium with the cell of position pos
        """
        # Gets the aquarium id
        aq_id = self.puzzle.pos_to_aq(pos)
        aq = self.puzzle.get_aquariums()[aq_id - 1]
        
        # Fills the desired aquarium
        if aq.can_fill():
            aq.fill_level()


    def _empty_level(self, pos):
        """Empties a level of the aquarium with the cell of position pos
        """
        aq_id = self.puzzle.pos_to_aq(pos)
        aq = self.puzzle.get_aquariums()[aq_id - 1]
        
        if aq.can_empty():
            aq.empty_level()


    def _reset(self):
        self.puzzle.set_done(False)
        for aquarium in self.puzzle.get_aquariums():
            aquarium.reset()
        

    def _check_solution(self):
        if ai_functions.objective_test(self.puzzle):
            self.puzzle.set_done(True)


    def _algorithm (self, event):
        """Starts the AI algorithm accordingly to event
        """

        # Bread First Search
        if event == AI.BFS:
            sol = ai_search.breadth_first_search(self.puzzle)
            self.puzzle.transform_into(sol.get_state())

        # Uniform Cost Search
        elif event == AI.UCS:
            sol = ai_search.uniform_cost_search(self.puzzle)
            self.puzzle.transform_into(sol.get_state())

        # Depth First Search
        elif event == AI.DFS:
            sol = ai_search.depth_first_search(self.puzzle)
            self.puzzle.transform_into(sol.get_state())

        # Iterative deepening
        elif event == AI.IDS:
            sol = ai_search.iterative_deepening_search(self.puzzle)
            self.puzzle.transform_into(sol.get_state())

        # Greedy algorithm
        elif event == AI.GREEDY:
            sol = ai_search.greedy_search(self.puzzle)
            self.puzzle.transform_into(sol.get_state())

        # A star
        elif event == AI.ASTAR:
            sol = ai_search.a_star(self.puzzle)
            self.puzzle.transform_into(sol.get_state())
