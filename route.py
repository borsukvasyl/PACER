class Route():
    def __init__(self, list, cost):
        self.nodes = list
        self.cost = cost

    @property
    def get_cost(self):
        return self.cost

    @property
    def get_nodes(self):
        return self.nodes
