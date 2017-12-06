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
        self.topk = PriorityQueue()
        self.compact_states = CompactStates()

    def find_topk_routes(self):
        """
        Finds topk routes.
        :return: PriorityQueue
        """
        self.topk = PriorityQueue()
        self.compact_states = CompactStates()

        initial_nodes = NodesSet({self.Q.get_start()})
        initial_compact_state = CompactState(self.find_gain(initial_nodes),
                                             [Route([self.Q.get_start()], 0)])
        self.compact_states.add_compact_state(initial_nodes, initial_compact_state)

        self._find_topk_routes(initial_nodes, NodesSet(self.VQ - {self.Q.get_start()}))
        return self.topk

    def _find_topk_routes(self, previous_nodes, prefix_nodes):
        """
        Finds topk routes.
        :return: None
        """
        for i in prefix_nodes:
            print(previous_nodes, i)
            nodes = NodesSet(previous_nodes | {i})
            print("nodes:", nodes)
            compact_state = CompactState(self.find_gain(nodes))
            for j in nodes:
                nodes_j = NodesSet(nodes - {j})
                print("nodes_j:", nodes_j, j)
                dominating_route = self.pruning1(nodes_j, j)
                route = dominating_route.extend_route(self.HIQ, j)
                if route.cost_to_node(self.HIQ, self.Q.get_finish()) < self.Q.get_budget():
                    UP = 0  # self.pruning2()
                    if compact_state.gain + UP >= self.topk.get()[0]:
                        compact_state.add_route(route)
            # updating topk
            self._find_topk_routes(nodes, prefix_nodes.get_prefix(i))

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

    def pruning1(self, nodes, node):
        """
        PACER's pruning-1.
        :param compact_states: CompactStates object
        :param nodes: set of POIs
        :param node: current POI
        :return: ---
        """
        routes = self.compact_states.get_compact_state(nodes).routes
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
