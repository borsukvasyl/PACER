from priority_queue import PriorityQueue
from compact_states.compact_states import CompactStates


class PACER(object):
    def __init__(self, Q, VQ, FIQ, HIQ):
        """
        Initializing PACER.
        :param Q: tuple(x, y, b, w, O, F)
        :param VQ: POI candidates
        :param FIQ: Feature Index
        :param HIQ: 2-Hop Index
        """
        self.Q = Q
        self.VQ = VQ
        self.FIQ = FIQ
        self.HIQ = HIQ
        self.topk = PriorityQueue()

    def find_topk_routes(self):
        """
        Finds topk routes.
        :return: ---
        """
        compact_states = CompactStates()
        # recursive call of _find_topk_routes
        pass

    def _find_topk_routes(self):
        """
        Finds topk routes.
        :return: ---
        """

    def find_gain(self, nodes):
        """
        Computes gain of given POIs.
        :param nodes: set of POIs
        :return: ---
        """
        pass

    def find_cost(self, route):
        """
        Computes cost of given route.
        :param route: Route object
        :return: ---
        """
        pass

    def pruning1(self, compact_states, nodes, node):
        """
        PACER's pruning-1.
        :param compact_states: CompactStates object
        :param nodes: set of POIs
        :param node: current POI
        :return: ---
        """
        routes = compact_states.get_compact_state(nodes).routes
        best_route = routes[0]
        best_cost = routes[0].cost_to_node(self.HIQ, node)
        if len(routes) > 1:
            for i in range(1, len(routes)):
                if best_cost > routes[i].cost_to_node(self.HIQ, node):
                    best_route = routes[i]
                    best_cost = routes[i].cost_to_node(self.HIQ, node)
        return best_route

    def pruning2(self):
        pass
