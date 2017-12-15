class CompactState(object):
    def __init__(self, gain, routes=None):
        """
        Initializing compact state.
        :param gain: gain of points
        :param routes: initial routes
        """
        self.gain = gain
        if routes is None:
            self.routes = []
        else:
            self.routes = routes

    def add_route(self, route):
        """
        Adds Route object to compact state.
        :param route: Route object
        :return: None
        """
        self.routes.append(route)

    def __repr__(self):
        """
        Returns string representation of CompactState
        :return: string representation
        """
        return str(self.routes)
