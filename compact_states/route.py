class Route(object):
    def __init__(self, route, cost):
        """
        Initializing route.
        :param route: list of points representing route
        :param cost: cost of this route
        """
        self.route = route
        self.cost = cost

    @staticmethod
    def travel_cost(HIQ, from_node, to_node):
        if to_node < from_node:
            from_node, to_node = to_node, from_node
        try:
            return HIQ[from_node][to_node]
        except KeyError:
            raise ValueError("No edge between nodes")

    def cost_to_node(self, HIQ, to_node):
        return self.cost + Route.travel_cost(HIQ, self.route[-1], to_node)

    def extend_route(self, HIQ,  node):
        new_cost = self.cost_to_node(HIQ, node)
        new_route = self.route + [node]
        return Route(new_route, new_cost)
