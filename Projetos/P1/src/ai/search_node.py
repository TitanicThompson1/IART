
class SearchNode:
    def __init__(self, state, predecessor, operator, depth, cost, heuristic):
        self.state = state
        self.predecessor = predecessor
        self.operator = operator
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic

    def get_path(self):
        return self.path

    def get_dist(self):
        return self.dist
   
    def get_value(self):
        return self.heuristic + self.cost

    def get_state(self):
        return self.state

    def get_depth(self):
        return self.depth


    def get_heuristic(self):
        return self.heuristic

    def get_cost(self):
        return self.cost

    def get_predecessor(self):
        return self.predecessor

    def get_heuristic(self):
        return self.heuristic



    def __str__(self):
        ret = "State: " + str(self.state) + "\n"
        ret += "Operator: " + str(self.operator) + "\n"
        ret += "Depth: " + str(self.depth) + "\n"
        ret += "Cost: " + str(self.cost) + "\n"
        ret += "Heuristic: " + str(self.heuristic) + "\n"
        return ret
    

    def __eq__(self, value):
    
        if not isinstance(value, SearchNode):
            return False
        
        return self.state == value.get_state()

    def __lt__(self, other):
        return self.cost < other.get_cost()