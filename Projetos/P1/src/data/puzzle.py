class Puzzle:
    """This class has the information about the puzzles, its aquarium, its size and its limits
    """
    def __init__(self, size: int, aquariums: list, limits: list):
        self.size = size
        self.aquariums = aquariums
        self.limits = limits
        self.done = False


    def is_done(self):
        return self.done
    

    def get_aquariums(self):
        return self.aquariums


    def get_limits(self):
        return self.limits


    def get_size(self):
        return self.size


    def get_n_filled(self, i, is_row):
        n_filled = 0
        for aq in self.aquariums:
            n_filled += aq.get_n_filled(i, is_row)
        
        return n_filled


    def set_done(self,done):
        self.done = done


    def substitute_aquarium(self, i, aq):
        self.aquariums.insert(i, aq)
        self.aquariums.pop(i + 1)


    def pos_to_aq(self, pos):
        """Given a cell position this function returns the aquarium it belongs to
        """
        for aq in self.aquariums:
            for cell in aq.cells:
                if cell.get_pos() == pos:
                    return aq.get_id()

    
    def transform_into(self, puzzle):
        """Transforms the puzzle into the puzzle passed as argument
        """
        
        self.aquariums = puzzle.get_aquariums()
        self.size = puzzle.get_size()
        self.limits = puzzle.get_limits()


    def __eq__(self, value):

        if not isinstance(value, Puzzle):
            return False
        
        return self.aquariums == value.get_aquariums()


    def __str__(self):
            ret =  str(self.size) + "\n"
            for aq in self.aquariums:
                ret += str(aq) + "\n"
            
            ret += str(self.limits)
            return ret
