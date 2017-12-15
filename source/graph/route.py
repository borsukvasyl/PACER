class Route(object):
    def __init__(self, route, cost):
        """
        Initializing route.
        :param route: list of points representing route
        :param cost: cost of this route
        """
        self.route = route
        self.cost = cost

    def get_first_node(self):
        """
        Gets first node from route.
        :return: first node in route
        """
        return self.route[0]

    def get_last_node(self):
        """
        Gets last node from route.
        :return: last node in route
        """
        return self.route[-1]

    @staticmethod
    def travel_cost(HIQ, from_node, to_node):
        """
        Calculates travel cost from 1'st node to 2'nd node.
        :param HIQ: HIQ
        :param from_node: 1'st node
        :param to_node: 2'nd node
        :return: cost between 1'st and 2'nd nodes
        """
        if to_node < from_node:
            from_node, to_node = to_node, from_node
        try:
            return HIQ[from_node][to_node]
        except KeyError:
            raise ValueError("No edge between nodes")

    def cost_to_node(self, HIQ, to_node):
        """
        Calculates travel cost of current route extended by new node.
        :param HIQ: HIQ
        :param to_node: new node
        :return: cost of new route
        """
        return self.cost + Route.travel_cost(HIQ, self.get_last_node(), to_node)

    def extend_route(self, HIQ,  node):
        """
        Extends current route by new node (doesn't change current route)
        :param HIQ: HIQ
        :param node: new node
        :return: new Route
        """
        new_cost = self.cost_to_node(HIQ, node)
        new_route = self.route + [node]
        return Route(new_route, new_cost)

    def __str__(self):
        """
        Returns string representation of Route
        :return: string representation
        """
        return "<cost={}, route={}>".format(self.cost, self.route)

    def __repr__(self):
        """
        Returns string representation of Route
        :return: string representation
        """
        return self.__str__()
