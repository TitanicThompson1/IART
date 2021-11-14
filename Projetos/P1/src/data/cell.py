ROW = 0
COL = 1

class Cell:
    """Class Cell stores cells info, the most basic piece of the puzzle
       its position(tuple) and if its filled
    """
    def __init__(self, pos):
        self.pos = pos
        self.is_filled = False


    def get_row(self):
        return self.pos[ROW]


    def get_col(self):
        return self.pos[COL]

    def get_pos(self):
        return self.pos

    
    def is_cell_filled(self):
        return self.is_filled 


    def fill_cell(self):
        """Function fills cell
        """
        self.is_filled = True


    def empty_cell(self):
        """Function empties cell
        """
        self.is_filled = False


    def __str__(self):
        return "Pos: {0} IsEmpty: {1}   \n".format(self.pos, self.is_filled)