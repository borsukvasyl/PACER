class Route(object):
    def __init__(self, route, cost):
        """
        Initializing route.
        :param route: list of points representing route
        :param cost: cost of this route
        """
        self.route = route
        self.cost = cost

    def cost_to_node(self, HIQ, node):
        return self.cost + HIQ[self.route[-1]][node]
