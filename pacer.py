from priority_queue import PriorityQueue
from compact_states.compact_states import CompactStates
from compact_states.compact_state import CompactState
from compact_states.route import Route
from compact_states.nodes_set import NodesSet


class PACER(object):
    def __init__(self, Q, VQ, FIQ, HIQ):
        """
        Initializing PACER.
        :param Q: Queue
        :param VQ: POI candidates
        :param FIQ: Feature Index
        :param HIQ: 2-Hop Index
        """
        self.Q = Q
        self.VQ = VQ
        self.FIQ = FIQ
        self.HIQ = HIQ
        # self.topk = PriorityQueue()

    def find_topk_routes(self):
        """
        Finds topk routes.
        :return: PriorityQueue
        """
        topk = PriorityQueue()
        compact_states = CompactStates()

        initial_nodes = {self.Q.get_start()}
        initial_compact_state = CompactState(self.find_gain(initial_nodes),
                                             [Route([self.Q.get_start], 0)])
        compact_states.add_compact_state(initial_nodes, initial_compact_state)

        self._find_topk_routes.topk = topk
        self._find_topk_routes.compact_states = compact_states
        self._find_topk_routes()
        return topk

    def _find_topk_routes(self, nodes_set, prefix_nodes):
        """
        Finds topk routes.
        :return: ---
        """
        self._find_topk_routes()

    def _compute_aggregation_f(self, feature, nodes):
        result = 0
        rank = 1
        elements = self.FIQ[feature]
        for ind in range(len(elements)):
            if elements[ind][0] in nodes:
                result += (rank ** (-self.Q.get_alpha())) * elements[ind][1]
                rank += 1
        return result

    def find_gain(self, nodes):
        """
        Computes gain of given POIs.
        :param nodes: set of POIs
        :return: ---
        """
        result = 0
        for feature in self.FIQ.keys():
            result += self.Q.get_preference()[feature] * self._compute_aggregation_f(feature, nodes)
        return result

    def pruning1(self, compact_states, nodes, node):
        """
        PACER's pruning-1.
        :param compact_states: CompactStates object
        :param nodes: set of POIs
        :param node: current POI
        :return: ---
        """
        routes = compact_states.get_compact_state(nodes).routes
        best_route = None
        best_cost = None
        for i in range(0, len(routes)):
            try:
                if best_route is None or best_cost > routes[i].cost_to_node(self.HIQ, node):
                    best_route = routes[i]
                    best_cost = routes[i].cost_to_node(self.HIQ, node)
            except ValueError:  # no edge to node
                continue
        return best_route

    def pruning2(self):
        pass
