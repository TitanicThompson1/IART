from .cell import *

class Aquarium: 
    """This class stores the information about an aquarium, its id, its maximum level
       its current level and all its cells
    """
    def __init__(self, id, max_level, current_level = 0, p_cells = None):
        self.id = id
        self.max_level = max_level
        
        self.current_level = current_level

        if p_cells == None:
            self.cells = []
        else:
            self.cells = p_cells
        

    def contains_cell(self, pos):
        """This function returns if a cell belongs to the aquarium
        """
        for cell in self.cells:
            if cell.get_pos() == pos:
                return True
        return False


    def reset(self):
        """Function makes aquarium empty and as such it empties every cell
        """
        self.current_level = 0
        for cell in self.cells:
            cell.empty_cell()



    def get_cur_lvl(self):
        return self.current_level

    
    def get_cells(self):
        return self.cells


    def get_id(self):
        return self.id


    def can_fill(self):
        """Funtion returns if its possible to fill the next level
        """
        return self.current_level < self.max_level


    def can_empty(self):
        """Function returns if its possible to empty curretn level
        """
        return self.current_level > 0


    def add_cell(self, cell):
        self.cells.append(cell)

    
    def fill_level(self):
        """Function fills next available level
        """
        row_to_fill = self._get_first_row_empty()
        
        for cell in self.cells:
            if cell.get_row() == row_to_fill:
                cell.fill_cell()

        self.current_level += 1


    def empty_level(self):
        """Function empties current level
        """
        row_to_empty = self._get_first_row_empty() - 1

        if row_to_empty < 0:
            row_to_empty = 0

        for cell in self.cells:
            if cell.get_row() == row_to_empty:
                cell.empty_cell()

        self.current_level -= 1
        

    def _get_first_row_empty(self):
        """Function return the first row (down/top) that is empty
        """
        cur_cell = None
        for cell in self.cells:
            cur_cell = cell
            if not cell.is_cell_filled():
                return cell.get_row()
        
        return cur_cell.get_row() + 1



    def get_n_filled(self, i, is_row):
        """Function returns how many horizontal or vertical cells are filled
        """
        n_filled = 0
        for cell in self.cells:
            
            if is_row:
                if cell.get_row() == i and cell.is_cell_filled():
                    n_filled += 1
            else: 
                if cell.get_col() == i and cell.is_cell_filled():
                    n_filled += 1

        return n_filled

    
    def __str__(self):
        ret = "ID: {0}   Max Level: {1} \n".format(self.id, self.max_level)

        for cell in self.cells:
            ret += str(cell) + "   "

        return ret


    def __eq__(self, value):
    
        if not isinstance(value, Aquarium):
            return False
        
        return self.current_level == value.get_cur_lvl()

