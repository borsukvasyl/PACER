import math

from source.compact_states.compact_state import CompactState
from source.compact_states.compact_states import CompactStates
from source.compact_states.nodes_set import NodesSet
from source.graph.route import Route
from source.queue.priority_queue import PriorityQueue


class PACER(object):
    def __init__(self, Q, VQ, FIQ, HIQ, k=10):
        """
        Initializing PACER.
        :param Q: Queue
        :param VQ: POI candidates
        :param FIQ: Feature Index
        :param HIQ: 2-Hop Index
        :param k: number of elements in priority queue
        """
        self.Q = Q
        self.VQ = VQ
        self.FIQ = FIQ
        self.HIQ = HIQ
        self.k = k

        self.topk = PriorityQueue()
        self.compact_states = CompactStates()

    def find_topk_routes(self):
        """
        Finds topk routes.
        :return: PriorityQueue
        """
        self.topk = PriorityQueue()
        self.compact_states = CompactStates()

        # setting initial compact state
        initial_compact_state = CompactState(self.find_gain(NodesSet({self.Q.get_start()})),
                                             [Route([self.Q.get_start()], 0)])
        self.compact_states.add_compact_state(NodesSet(), initial_compact_state)

        self._find_topk_routes(NodesSet(), NodesSet(self.VQ - {self.Q.get_start(), self.Q.get_finish()}))
        return self.topk

    def _find_topk_routes(self, previous_nodes, prefix_nodes):
        """
        Finds topk routes.
        :param previous_nodes: set of previous POIs
        :param prefix_nodes: available POIs
        :return: None
        """
        # extending previous_nodes, by one node from prefix_nodes
        for i in prefix_nodes:
            nodes = NodesSet(previous_nodes | {i})
            compact_state = CompactState(self.find_gain(nodes))
            print("nodes: {}, previous: {}, prefix: {}".format(nodes, previous_nodes, prefix_nodes))

            # computing best routes
            for j in nodes:
                # finding best route for ending point in j (pruning-1)
                nodes_j = NodesSet(nodes - {j})
                dominating_route = self.pruning1(nodes_j, j)
                if dominating_route is None:
                    continue
                route = dominating_route.extend_route(self.HIQ, j)
                print(">nodes_{}:".format(j), nodes_j, dominating_route, route)

                # checking whether gain of this route is valid (pruning-2)
                if route.cost_to_node(self.HIQ, self.Q.get_finish()) < self.Q.get_budget():
                    UP = self.pruning2(route)
                    if compact_state.gain + UP >= self._get_topk_kth_element():
                        compact_state.add_route(route)
                    #compact_state.add_route(route)  # to remove #
            self.updata_topk(compact_state)
            self.compact_states.add_compact_state(nodes, compact_state)
            self._find_topk_routes(nodes, prefix_nodes.get_prefix(i))

    def _compute_aggregation_f(self, feature, nodes):
        """
        Computes feature aggregation function.
        :param feature: computing feature
        :param nodes: set of nodes
        :return: feature aggregation function result
        """
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
        """
        Find difference of gains of two sets
        :param set_1: set of nodes
        :param set_2: set of nodes
        :return: float
        """
        return self.find_gain(set_1) - self.find_gain(set_2)

    def pruning1(self, nodes, node):
        """
        PACER's pruning-1.
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
        """
        Realization of pruning 2 from article
        Finds value of UP required for checking the rule:
        Gain(current_route) + UP > Gain(topK(k))
        :param current_route: object of class Route
        :return: float
        """
        UP = 0
        # Find U: set of remaining nodes travel cost to which is less
        # than remaining budget
        remaining_budget = self._find_remaining_budget(self.Q.get_budget(), current_route.cost)
        last_node_on_route = current_route.get_last_node()
        unvisited_nodes_set = set(self.VQ).difference(set(current_route.route)). \
            difference({self.Q.get_finish()})
        valid_nodes_set_u = self._find_remaining_valid_nodes_set(last_node_on_route,
                                                                 unvisited_nodes_set, remaining_budget)

        # Find each node r and beta value
        rs_dict = {}
        betas_dict = {}
        for node in valid_nodes_set_u.union({self.Q.get_finish()}):
            beta = self._find_delta_gain({node}, set(current_route.route)) - \
                   self._find_delta_gain(set(), current_route.route)
            betas_dict[node] = beta
            c = self._find_node_set_cost(node, current_route.get_last_node())
            r = beta / c
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

        if sorted_valid_nodes:
            l = len(sorted_valid_nodes)
            if current_sum > B:
                l_node = sorted_valid_nodes.pop()
                current_sum -= self._find_node_set_cost(l_node, last_node_on_route)
                bound = l - 1
            else:
                l_node = sorted_valid_nodes[-1]
                bound = l

            l_c = self._find_node_set_cost(l_node, last_node_on_route)
            lammbda = (B - current_sum) / l_c

            # Find UP value
            j = 0
            while j < bound:
                UP += betas_dict[sorted_valid_nodes[j]]
                j += 1
            UP += lammbda * betas_dict[l_node]

        return UP

    @staticmethod
    def _find_remaining_budget(travel_budget, path_cost):
        """
        Compute difference of two values
        :param travel_budget: int
        :param path_cost: int
        :return: int
        """
        return travel_budget - path_cost

    def _find_remaining_valid_nodes_set(self, last_node_on_route, unvisited_nodes_set, remaining_budget):
        """
        :param last_node_on_route: index of last node on route
        :param unvisited_nodes_set: set of remaining nodes(other from the ones on the route)
        :param remaining_budget: int
        :return: set of nodes, which are connected with both last node on route and final point
        """
        result_set = set()
        for node in unvisited_nodes_set:
            finish = self.Q.get_finish()
            try:
                if Route.travel_cost(self.HIQ, last_node_on_route, node) + \
                        Route.travel_cost(self.HIQ, node, finish) <= remaining_budget:
                    result_set.add(node)
            except ValueError:
                pass

        return result_set

    def _find_node_set_cost(self, node, last_node_in_route):
        """
        Cost of node on the remaining route
        :param node: index, int
        :param last_node_in_route: index, int
        :return: float
        """
        try:
            incoming_travel_cost = Route.travel_cost(self.HIQ, last_node_in_route, node)
        except ValueError:
            incoming_travel_cost = math.inf

        try:
            outcoming_travel_cost = Route.travel_cost(self.HIQ, node, self.Q.get_finish())
        except ValueError:
            outcoming_travel_cost = math.inf

        return (incoming_travel_cost + outcoming_travel_cost) / 2 + 1.0

    def _get_topk_kth_element(self):
        if self.topk.size() < self.k:
            return 0
        return self.topk.get_by_index_priority(self.k - 1)[1]

    def updata_topk(self, compact_state):
        for route in compact_state.routes:
            self.topk.put((route, compact_state.gain))
