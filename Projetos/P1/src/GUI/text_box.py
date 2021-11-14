
SCREEN = 0
FONT = 1
COLOR = (0, 0, 0)
BCKG_COLOR = (200, 200, 200)
HEIGHT = 20
WIDHT_PER_LETTER = 9.6

class TextBox:
    """ Data class with the a text box. A default background color and font color is defined.
    """

    def __init__(self, game_chars, display_info, action = None, background_color = (16, 117, 232), color = (255, 255, 255)):

        self.screen = game_chars[SCREEN]
        self.box = game_chars[FONT].render(display_info[1], True, color, background_color)
        self.pos = display_info[0]
        self.width = len(display_info[1]) * WIDHT_PER_LETTER
        self.action = action
        
    
    def display(self):
        self.screen.blit(self.box, self.pos)


    def get_action(self):
        return self.action


    def check_clicked(self, pos_clckd):
        return self._check_width_rng(pos_clckd) and self._check_height_rng(pos_clckd)


    def _check_width_rng(self, pos_clckd):
        return pos_clckd[0] >= self.pos[0] and pos_clckd[0] <= self.pos[0] + self.width


    def _check_height_rng(self, pos_clckd):
        return pos_clckd[1] >= self.pos[1] and pos_clckd[1] <= self.pos[1] + HEIGHT


        