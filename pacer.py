import math

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

        initial_compact_state = CompactState(self.find_gain(NodesSet({self.Q.get_start()})),
                                             [Route([self.Q.get_start()], 0)])
        self.compact_states.add_compact_state(NodesSet(), initial_compact_state)

        self._find_topk_routes(NodesSet(), NodesSet(self.VQ - {self.Q.get_start()}))
        return self.topk

    def _find_topk_routes(self, previous_nodes, prefix_nodes):
        """
        Finds topk routes.
        :return: None
        """
        for i in prefix_nodes:
            nodes = NodesSet(previous_nodes | {i})
            print("nodes: {}, previous: {}, prefix: {}".format(nodes, previous_nodes, prefix_nodes))
            compact_state = CompactState(self.find_gain(nodes))
            for j in nodes:
                nodes_j = NodesSet(nodes - {j})
                dominating_route = self.pruning1(nodes_j, j)
                if dominating_route is None:
                    continue
                route = dominating_route.extend_route(self.HIQ, j)
                print(">nodes_{}:".format(j), nodes_j, dominating_route, route)
                if route.cost_to_node(self.HIQ, self.Q.get_finish()) < self.Q.get_budget():
                    compact_state.add_route(route)  # remove this line
                    # UP = 0  # self.pruning2()
                    # if compact_state.gain + UP >= self.topk.get()[0]:
                    #     compact_state.add_route(route)
            # updating topk
            self.compact_states.add_compact_state(nodes, compact_state)
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

    def _find_delta_gain(self, set_1, set_2):
        return self.find_gain(set_1) - self.find_gain(set_2)

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
                    try:
                        best_cost = routes[i].cost_to_node(self.HIQ, node)
                    except ValueError:
                        best_route = None
            except ValueError:  # no edge
                continue
        return best_route

    def pruning2(self, current_route):
        # Find U: set of remaining nodes travel cost to which is less
        # than remaining budget
        remaining_budget = self._find_remaining_budget(self.Q.get_budget(), current_route.cost)
        last_node_on_route = current_route.get_last_node()
        unvisited_nodes_set = set(self.VQ).difference(set(current_route.route)).\
            difference({self.Q.get_finish()})
        valid_nodes_set_u = self._find_remaining_valid_nodes_set(last_node_on_route,
                                                               unvisited_nodes_set, remaining_budget)

        # Find each node r and beta value
        rs_dict = {}
        betas_dict = {}
        for node in valid_nodes_set_u.union(self.Q.get_finish()):
            beta = self._find_delta_gain({node}, set(current_route.route)) - \
                self._find_delta_gain(set(), current_route)
            betas_dict[node] = beta
            c = self._find_node_set_cost(node, current_route.get_last_node())
            r = beta // c
            rs_dict[node] = r
        sorted_nodes = sorted(rs_dict.keys(), key=rs_dict.get, reverse=True)

        # Find lambda and l values required
        # for computation of UP value
        current = current_sum = 0
        sorted_valid_nodes = []
        c_of_last_node_in_route = self._find_node_set_cost(last_node_on_route,
                                                            last_node_on_route)
        c_of_last_node_in_route = c_of_last_node_in_route \
            if c_of_last_node_in_route != math.inf else 0
        B = remaining_budget - c_of_last_node_in_route
        while current < len(sorted_nodes) and current_sum <= B:
            node_set_cost = self._find_node_set_cost(sorted_nodes[current],
                                                    last_node_on_route)
            if node_set_cost == math.inf:
                current += 1
                continue
            current_sum += node_set_cost
            sorted_valid_nodes.append(sorted_nodes[current])
            current += 1
        l = len(sorted_valid_nodes)
        l_c = self._find_node_set_cost(sorted_nodes[current], last_node_on_route)
        l_c = l_c if l_c != math.inf else remaining_budget - \
                                          self._find_node_set_cost(sorted_valid_nodes[-1], last_node_on_route) + 1
        lammbda = (B - current_sum) // l_c

        # Find UP value
        UP = 0
        j = 0
        while j < l - 1:
            UP += betas_dict[sorted_valid_nodes[j]]
            j += 1
        UP += lammbda * betas_dict[sorted_valid_nodes[j]]
        return UP


    @staticmethod
    def _find_remaining_budget(travel_budget, path_cost):
        return travel_budget - path_cost

    def _find_remaining_valid_nodes_set(self, last_node_on_route, unvisited_nodes_set, remaining_budget):
        result_set = set()
        for node in unvisited_nodes_set:
            finish = self.Q.get_finish()
            if Route.travel_cost(self.HIQ, last_node_on_route, node) + \
                Route.travel_cost(self.HIQ, node, finish) <= remaining_budget:
                result_set.add(node)

        return result_set

    def _find_node_set_cost(self, node, last_node_in_route):
        try:
            incoming_travel_cost = Route.travel_cost(self.HIQ, last_node_in_route, node)
        except ValueError:
            incoming_travel_cost = math.inf

        try:
            outcoming_travel_cost = Route.travel_cost(self.HIQ, node, self.Q.get_finish())
        except ValueError:
            outcoming_travel_cost = math.inf

        return (incoming_travel_cost + outcoming_travel_cost) // 2
