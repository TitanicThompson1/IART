import pygame
import copy
import math


from .action import Action
from .action_ai import *
from .action_move import ActionMove
from .my_event import MyEvent
from .text_box import TextBox

import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../puzzles/test_puzzle2.pzl"
abs_file_path = os.path.join(script_dir, rel_path)

OFFSET_X = 70
OFFSET_Y = 400
OFFSET_X_BUTTONS = 500
OFFSET_X_LIMITS = 30
OFFSET_Y_LIMITS = 310

CELL_HEIGHT = 40
CELL_WIDTH = 40


class Gui:
    """This class allows to represent the game using the library Pygame
    """
    
    def __init__(self, puzzle):

        self.puzzle = puzzle


        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption("Aquarium")

        # Images of the cells
        self.empty_cell = pygame.image.load( os.path.join(script_dir,'./images/empty_cell.PNG'))
        self.filled_cell = pygame.image.load(os.path.join(script_dir,'./images/filled_cell.PNG'))

        # Image of the borders
        self.v_barrier = pygame.image.load(os.path.join(script_dir,'./images/v_barrier.jpg'))
        self.h_barrier = pygame.image.load(os.path.join(script_dir,'./images/h_barrier.jpg'))

        # Image of the borders
        self.limit_0 = pygame.image.load(os.path.join(script_dir,'./images/limit_0.PNG'))
        self.limit_1 = pygame.image.load(os.path.join(script_dir,'./images/limit_1.PNG'))
        self.limit_2 = pygame.image.load(os.path.join(script_dir,'./images/limit_2.PNG'))
        self.limit_3 = pygame.image.load(os.path.join(script_dir,'./images/limit_3.PNG'))
        self.limit_4 = pygame.image.load(os.path.join(script_dir,'./images/limit_4.PNG'))
        self.limit_5 = pygame.image.load(os.path.join(script_dir,'./images/limit_5.PNG'))
        self.limit_6 = pygame.image.load(os.path.join(script_dir,'./images/limit_6.PNG'))
        self.limit_7 = pygame.image.load(os.path.join(script_dir,'./images/limit_7.PNG'))
        self.limit_8 = pygame.image.load(os.path.join(script_dir,'./images/limit_8.PNG'))
        self.limit_9 = pygame.image.load(os.path.join(script_dir,'./images/limit_9.PNG'))

        # Font of the game
        self.font = pygame.font.Font('freesansbold.ttf', 18)

        self.clock = pygame.time.Clock()

        
        # All buttons 
        reset_btn = TextBox([self.screen, self.font], ((OFFSET_X_BUTTONS, 400), "Reset puzzle"), Action(MyEvent.RESET))
        check_sol_btn = TextBox([self.screen, self.font], ((OFFSET_X_BUTTONS, 450), "Check solution"), Action(MyEvent.CHCK_SOL))

        # AI buttons    
        bfs_button = TextBox([self.screen, self.font],((OFFSET_X_BUTTONS, 85), "Breath First Search"), ActionAI(AI.BFS))
        dps_button = TextBox([self.screen, self.font],((OFFSET_X_BUTTONS, 135), "Depth First Search"), ActionAI(AI.DFS))
        ucs_button = TextBox([self.screen, self.font],((OFFSET_X_BUTTONS, 185), "Uniform Cost Search"), ActionAI(AI.UCS))
        ids_button = TextBox([self.screen, self.font],((OFFSET_X_BUTTONS, 235), "Iterative Deepening Search"), ActionAI(AI.IDS))
        gs_button = TextBox([self.screen, self.font],((OFFSET_X_BUTTONS, 285), "Greedy Search"), ActionAI(AI.GREEDY))
        asa_button = TextBox([self.screen, self.font],((OFFSET_X_BUTTONS, 335), "A* Algortihm"), ActionAI(AI.ASTAR))

        # Control puzzle buttons
        next_button = TextBox([self.screen, self.font],((OFFSET_X + 80, OFFSET_Y + 70), "Next"), Action(MyEvent.N_PZL))
        prev_button = TextBox([self.screen, self.font],((OFFSET_X - 10, OFFSET_Y + 70), "Previous"), Action(MyEvent.P_PZL))


        self.buttons = [reset_btn, check_sol_btn, bfs_button, dps_button, ucs_button, ids_button, gs_button, asa_button, next_button, prev_button]

        self.correct = TextBox([self.screen, self.font],((500, 500 ), "Correct!!!"), background_color= (255, 255, 255))

        # Initial draw
        self._draw()


    def _draw(self):
        """Draws all of the game
        """
        # Clean the screen
        self.screen.fill((255, 255, 255))

        # Draws the puzzle
        self._draw_puzzle()
        
        # Draws all the buttons
        self._draw_buttons()
        
        # Draws all the barriers
        self._draw_barriers()

        # Draws all the limits
        self._draw_limits()


    def _draw_barriers(self):
        size = self.puzzle.get_size()
        

        for aq in self.puzzle.get_aquariums():
            for cell in aq.get_cells():
                cur_pos = cell.get_pos()

                # Draws left barrier
                if cur_pos[1] > 0 and not aq.contains_cell((cur_pos[0], cur_pos[1] - 1)):
                    self.screen.blit(self.v_barrier, (OFFSET_X + cur_pos[1] * CELL_WIDTH, OFFSET_Y - cur_pos[0] * CELL_HEIGHT))

                # Draws right barrier
                if cur_pos[1] < size - 1 and not aq.contains_cell((cur_pos[0], cur_pos[1] + 1)):
                    self.screen.blit(self.v_barrier, (OFFSET_X + cur_pos[1] * CELL_WIDTH + CELL_WIDTH, OFFSET_Y - cur_pos[0] * CELL_HEIGHT))

                # Draws bottom barrier
                if cur_pos[0] > 0 and not aq.contains_cell((cur_pos[0] - 1, cur_pos[1])):
                   self.screen.blit(self.h_barrier, (OFFSET_X + cur_pos[1] * CELL_WIDTH, OFFSET_Y - cur_pos[0] * CELL_HEIGHT + CELL_HEIGHT))

                # Draws top barrier
                if cur_pos[0] < size - 1 and not aq.contains_cell((cur_pos[0] + 1, cur_pos[1])):
                    self.screen.blit(self.h_barrier, (OFFSET_X + cur_pos[1] * CELL_WIDTH, OFFSET_Y - cur_pos[0] * CELL_HEIGHT))

    
    def _draw_buttons(self):
        for btn in self.buttons:
            btn.display()

    def _draw_puzzle(self):
        
        size = self.puzzle.get_size()

        if self.puzzle.is_done():
            self.correct.display()
            

        for aq in self.puzzle.get_aquariums():
            for cell in aq.get_cells():
                if cell.is_cell_filled():
                    self.screen.blit(self.filled_cell, (OFFSET_X + cell.get_col() * CELL_WIDTH, OFFSET_Y - cell.get_row() * CELL_HEIGHT))
                else:
                    self.screen.blit(self.empty_cell, (OFFSET_X + cell.get_col() * CELL_HEIGHT, OFFSET_Y - cell.get_row() * CELL_HEIGHT))
    
    def _draw_limits(self):

        size = self.puzzle.get_size()
        i = 0
        for h_limit in self.puzzle.get_limits()[0]:
            if h_limit == 0:
                self.screen.blit(self.limit_0, (OFFSET_X + CELL_WIDTH * i, OFFSET_Y - CELL_HEIGHT * size))
            elif h_limit == 1:
                self.screen.blit(self.limit_1, (OFFSET_X + CELL_WIDTH * i, OFFSET_Y - CELL_HEIGHT * size))
            elif h_limit == 2:
                self.screen.blit(self.limit_2, (OFFSET_X + CELL_WIDTH * i, OFFSET_Y - CELL_HEIGHT * size))
            elif h_limit == 3:
                self.screen.blit(self.limit_3, (OFFSET_X + CELL_WIDTH * i, OFFSET_Y - CELL_HEIGHT * size))
            elif h_limit == 4:
                self.screen.blit(self.limit_4, (OFFSET_X + CELL_WIDTH * i, OFFSET_Y - CELL_HEIGHT * size))
            elif h_limit == 5:
                self.screen.blit(self.limit_5, (OFFSET_X + CELL_WIDTH * i, OFFSET_Y - CELL_HEIGHT * size))
            elif h_limit == 6:
                self.screen.blit(self.limit_6, (OFFSET_X + CELL_WIDTH * i, OFFSET_Y - CELL_HEIGHT * size))
            elif h_limit == 7:
                self.screen.blit(self.limit_7, (OFFSET_X + CELL_WIDTH * i, OFFSET_Y - CELL_HEIGHT * size))
            elif h_limit == 8:
                self.screen.blit(self.limit_8, (OFFSET_X + CELL_WIDTH * i, OFFSET_Y - CELL_HEIGHT * size))
            elif h_limit == 9:
                self.screen.blit(self.limit_9, (OFFSET_X + CELL_WIDTH * i, OFFSET_Y - CELL_HEIGHT * size))
            i += 1
        
        i = 0
        for v_limit in self.puzzle.get_limits()[1]:
            if v_limit == 0:
                self.screen.blit(self.limit_0, (OFFSET_X_LIMITS, OFFSET_Y - CELL_HEIGHT * i))
            elif v_limit == 1:
                self.screen.blit(self.limit_1, (OFFSET_X_LIMITS, OFFSET_Y - CELL_HEIGHT * i))
            elif v_limit == 2:
                self.screen.blit(self.limit_2, (OFFSET_X_LIMITS, OFFSET_Y - CELL_HEIGHT * i))
            elif v_limit == 3:
                self.screen.blit(self.limit_3, (OFFSET_X_LIMITS, OFFSET_Y - CELL_HEIGHT * i))
            elif v_limit == 4:
                self.screen.blit(self.limit_4, (OFFSET_X_LIMITS, OFFSET_Y - CELL_HEIGHT * i))
            elif v_limit == 5:
                self.screen.blit(self.limit_5, (OFFSET_X_LIMITS, OFFSET_Y - CELL_HEIGHT * i))
            elif v_limit == 6:
                self.screen.blit(self.limit_6, (OFFSET_X_LIMITS, OFFSET_Y - CELL_HEIGHT * i))
            elif v_limit == 7:
                self.screen.blit(self.limit_7, (OFFSET_X_LIMITS, OFFSET_Y - CELL_HEIGHT * i))
            elif v_limit == 8:
                self.screen.blit(self.limit_8, (OFFSET_X_LIMITS, OFFSET_Y - CELL_HEIGHT * i))
            elif v_limit == 9:
                self.screen.blit(self.limit_9, (OFFSET_X_LIMITS, OFFSET_Y - CELL_HEIGHT * i))
            i += 1
        
        

            
    def _get_cell_pos(self, clicked_pos):
        pos = list(clicked_pos)
        pos[0] = pos[0] - OFFSET_X   
        pos[1] = pos[1] - OFFSET_Y 
        res = []

        res.append(math.floor(pos[1] / CELL_HEIGHT))        
        res.append( math.floor(pos[0] / CELL_WIDTH))
        
        res[0] = -res[0]

        return tuple(res)
        

    def get_action(self):

        # Gets all pygame events
        for event in pygame.event.get():

            # If user closes the window
            if event.type == pygame.QUIT:
                return Action(MyEvent.QUIT)
            
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # LEFTCLICK
                
                # Checks if user clicked on any button
                for btn in self.buttons:
                    if btn.check_clicked(event.pos):
                        if btn.get_action() == MyEvent.RESET:
                            self._reset()
                        return btn.get_action()
                
                # Checks if user clicked on the puzzle (Left click means fill aquarium )
                if self._check_puzzle_clckd(event.pos):
                    return ActionMove(MyEvent.FILL, self._get_cell_pos(copy.copy(event.pos)))
            
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # RIGHTCLICK
                # Checks if user clicked on the puzzle (Right click means empty aquarium )
                if self._check_puzzle_clckd(event.pos):
                    return ActionMove(MyEvent.EMPTY, self._get_cell_pos(copy.copy(event.pos)))
            
        return Action(MyEvent.NOEVENT)


    def _check_puzzle_clckd(self, pos):
        return self._check_x_pzzl_clckd(pos) and self._check_y_pzzl_clckd(pos)


    def _check_x_pzzl_clckd(self, pos):
        return pos[0] > OFFSET_X and pos[0] <= OFFSET_X + self.puzzle.get_size() * CELL_WIDTH

    
    def _check_y_pzzl_clckd(self, pos):
        return pos[1] < OFFSET_Y + CELL_HEIGHT and pos[1] > OFFSET_Y - (self.puzzle.get_size() - 1)* CELL_HEIGHT


    def display(self):
        self._draw()

        pygame.display.update()

        # Set FPS to 40
        self.clock.tick(40)

    def close(self):
        pygame.quit()

        