import copy
INF = 100000

def objective_test(state):
    """Function to evaluate if puzzle has been solved
    """
    h_limits = state.get_limits()[0]
    v_limits = state.get_limits()[1]

    for i, hl in enumerate(h_limits):
        if not hl == state.get_n_filled(i, False):
            
            return False
    
    for j, vl in enumerate(v_limits):
        if not vl == state.get_n_filled(j, True):
            
            return False
    
    return True



def precond(aquarium, oper):
    """Function that returns if is possible to empty or fill a level
    """
    if oper == "Fill":
        return aquarium.can_fill()
        
    elif oper == "Empty":
        return aquarium.can_empty()
    
    else:
        print("Error in precond: Invalid Oper")
        return False



def effects(aquarium, oper):
    """Function that apllies and operand in order to fill or empty a level of an aquarium
    """
    aquarium_cpy = copy.deepcopy(aquarium)
    if oper == "Fill":
        aquarium_cpy.fill_level()
    elif oper == "Empty":
        aquarium_cpy.empty_level()

    return aquarium_cpy



def heuristic_1(puzzle):
    """ This heuristic returns the sum of the absolute difference between the desired number of cells 
    filled in each row/column and the actual number of filled cells.
    """
    puzzle_size = puzzle.get_size()
    h_limits = puzzle.get_limits()[0]       # Horizontal limits
    v_limits = puzzle.get_limits()[1]       # Vertical limits
    hrz_heur = []                           
    vrt_heur = []

    for i in range(puzzle_size):
        cells_filled = puzzle.get_n_filled(i, False)
        hrz_heur.append(abs(cells_filled - h_limits[i]))

    for i in range(puzzle_size):
        cells_filled = puzzle.get_n_filled(i, True)
        vrt_heur.append(abs(cells_filled - v_limits[i]))
        
    return sum(hrz_heur) + sum(vrt_heur)


def heuristic_2(puzzle):
    """ This heuristic sums all the rows and columns that are not correct, i.e., 
    the number of filled cells are different from the goal
    """
    puzzle_size = puzzle.get_size()
    h_limits = puzzle.get_limits()[0]
    v_limits = puzzle.get_limits()[1]
    heuristic = 0

    for i in range(puzzle_size):
        if h_limits[i] != puzzle.get_n_filled(i, False):
            heuristic += 1

    for i in range(puzzle_size):
        if v_limits[i] != puzzle.get_n_filled(i, True):
            heuristic += 1
        
    return heuristic  

def heuristic_3(puzzle):
    """ This heuristic is an improvement to the first heuristic. When the number of filled cells is greater than the goal, 
    the solution is unviable and the heuristic of that node is set to a large number

    """
    puzzle_size = puzzle.get_size()
    h_limits = puzzle.get_limits()[0]
    v_limits = puzzle.get_limits()[1]
    hrz_heur = []
    vrt_heur = []

    for i in range(puzzle_size):
        cells_filled = puzzle.get_n_filled(i, False)
        to_add = _calculate_value_h(cells_filled, h_limits[i])
        if to_add == INF:
            return INF
        hrz_heur.append(to_add)

    for i in range(puzzle_size):
        cells_filled = puzzle.get_n_filled(i, True)
        to_add = _calculate_value_h(cells_filled, v_limits[i])
        if to_add == INF:
            return INF
        vrt_heur.append(to_add)
        
    return sum(hrz_heur) + sum(vrt_heur)



def _calculate_value_h(n_flld_cells, limit):
    """Calculates the heuristic value for the third heuristic
    """
    if n_flld_cells > limit:
        return INF
        
    return abs(n_flld_cells - limit)