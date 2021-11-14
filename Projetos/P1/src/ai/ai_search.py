from .search_node import *
from .ai_functions import *
from queue import PriorityQueue


from data.puzzle import *
from data.cell import *
from data.aquarium import *

OPER1 = "Fill"

"""Note: For all algorithm, we don't need to search for a repeated state, because it is impossible for two states from the same search 
space to be the same (since we only have one operator)
"""


def breadth_first_search(puzzle):
    root = SearchNode(puzzle, None, None, 0, 0, 0)

    queue = [root]

    while len(queue) != 0:

        # Get next node
        current_node = queue[0]

        # If it is the objective node
        if objective_test(current_node.get_state()): 
            break

        # Removes node from queue
        queue.pop(0)
        
        children = generate_children(current_node)

        for child in children:
            queue.append(child)
    
    if len(queue) == 0:
        return "Didn't found a solution"

    return queue[0]



def uniform_cost_search(puzzle):
    root = SearchNode(puzzle, None, None, 0, 0, 0)
    
    # Initializing priority queue. This queue sorts the elements (a tuple (Key, Valye) ) by ascending order of the Key 
    p_queue = PriorityQueue()

    # In UCS, the value that we want to sort by is the cost to get to the node
    p_queue.put((root.get_cost(), root))

    solution = None
    while not p_queue.empty():
        
        # The function get already deletes the node from the queue
        current_node = p_queue.get()[1]

        if objective_test(current_node.get_state()): 
            solution = current_node
            break
        
        children = generate_children(current_node)

        for child in children:            
            p_queue.put((child.get_cost(), child))
    
    if p_queue.empty():
        return "Didn't found a solution"

    return solution


def depth_first_search(puzzle):
    root = SearchNode(puzzle, None, None, 0, 0, 0)

    # We implemented the DFS algorithm using a recursion
    return recursive_dfs(root)


def recursive_dfs(current_node):


    if objective_test(current_node.get_state()):
        return current_node

    children = generate_children(current_node)

   
    for child in children:
        solution = recursive_dfs(child)
        if solution != None:
                return solution
    
    return None


def iterative_deepening_search(puzzle):
    root = SearchNode(puzzle, None, None, 0, 0, 0)

    i = 0
    solution = None

    # The maximum depth is incremented by one every time the algorithm does not find a solution
    while solution == None:
        solution  = recursive_ids(root, i)
        i += 1
    
    return solution


def recursive_ids(current_node, max_depth):
    if objective_test(current_node.get_state()):
        return current_node

    children = generate_children(current_node)
    for child in children:
        if child.get_depth() <= max_depth:
            solution = recursive_ids(child, max_depth)

            if solution != None:
                return solution

    
    return None     # Didn't find a solution




def greedy_search(puzzle):

    root = SearchNode(puzzle, None, None, 0, 0, heuristic_3(puzzle))
    pqueue = PriorityQueue()
    obj = root

    pqueue.put((root.get_heuristic() , root))

    while not pqueue.empty():

        closest_child = pqueue.get()[1]
        children = generate_children(closest_child)

        if objective_test(closest_child.get_state()): 
            obj = closest_child
            break

        
        for child in children:
                pqueue.put((child.get_heuristic(), child))

    if pqueue.empty():
        return "Didn't found a solution"

    return obj



def a_star(puzzle):
    root = SearchNode(puzzle, None, None, 0, 0, heuristic_3(puzzle))
    pqueue = PriorityQueue()
    obj = root

    pqueue.put((root.get_value() , root))

    while not pqueue.empty():

        closest_child = pqueue.get()[1]

        if objective_test(closest_child.get_state()): 
            obj = closest_child
            break

        children = generate_children(closest_child)

        for child in children:
            pqueue.put((child.get_value(), child))      # get_value function returns the cost plus the heuristic

    if pqueue.empty():
        return "Didn't found a solution"

    return obj



def generate_children(node):
    """ This function generates all the children nodes of node
    """
    res = []

    puzzle = node.get_state()

  

    for i, aq in enumerate(puzzle.get_aquariums()):
        if precond(aq, OPER1):
            
            # Creates a new aquarium with the applied effect 
            new_aq = effects(aq, OPER1)
            
            # A copy is made in order to not change the original
            puzzle_cpy = copy.deepcopy(puzzle)

            puzzle_cpy.substitute_aquarium(i, new_aq)

            new_node = SearchNode(puzzle_cpy, node, OPER1, node.get_depth() + 1,  node.get_cost() + 1, heuristic_3(puzzle_cpy))
            res.append(new_node)

        
    return res