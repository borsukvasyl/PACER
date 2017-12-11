class GraphInterface:
    """
    Created to simplify manipulations with possibly unfamiliar graph
    """
    class Node:
        class Neighbour:
            def __init__(self, i, c):
                self._index = i
                self._cost = c

            def __repr__(self):
                return "Neighbour(index={0}, cost={1})".format(self._index, self._cost)

            def get_index(self):
                return self._index

            def get_cost(self):
                return self._cost

        # Node code begins
        def __init__(self, i, fv, lst):
            """

            :param i: integer index of node
            :param fv: tuple, feature vector
            :param lst: list(tuple), list of neighbours
            """
            self._node_index = i
            self._feature_vector = fv
            self._neighbours = self._create_neighbours(lst)

        def __repr__(self):
            return "Node({})".format(self._node_index)

        def get_index(self):
            return self._node_index

        def get_feature_vector(self):
            return self._feature_vector

        def get_neighbours(self):
            return self._neighbours

        @staticmethod
        def get_neighbour_index(neighbour):
            return neighbour.get_index()

        @staticmethod
        def get_neighbour_cost(neighbour):
            return neighbour.get_cost()

        @staticmethod
        def _create_neighbours(lst):
            neighbours = []
            for pair in lst:
                neighbour = GraphInterface.Node.Neighbour(pair[0], pair[1])
                neighbours.append(neighbour)
            return neighbours

    # GrapInterface code begins
    def __init__(self, feature_number):
        self.nodes = []
        self._feature_number = feature_number
        self._build_graph(None) #TODO: write this function

    def get_nodes(self):
        for node in self.nodes:
            yield node

    def get_feature_number(self):
        return self._feature_number

    @staticmethod
    def get_node_index(node):
        return node.get_index()

    @staticmethod
    def get_node_feature_vector(node):
        return node.get_feature_vector()

    @staticmethod
    def get_node_neighbours(node):
        return node.get_neighbours()

    @staticmethod
    def get_node_neighbour_index(neighbour):
        return GraphInterface.Node.get_neighbour_index(neighbour)

    @staticmethod
    def get_node_neighbour_cost(neighbour):
        return GraphInterface.Node.get_neighbour_cost(neighbour)

    def _build_graph(self, graph):
        """
        #TODO: WRITE USING IGRAPH LIBRARY http://igraph.org/python/doc/igraph.GraphBase-class.html
        Build graph interface from graph from other library
        :param graph: some object of graph from foreign library
        :return:
        """
        node1 = GraphInterface.Node(0, (0.6, 0.8, 0.1), [(1, 5), (2, 4)])
        node2 = GraphInterface.Node(1, (0.0, 1.0, 0.9), [(0, 5)])
        node3 = GraphInterface.Node(2, (0.1, 0.3, 0.0), [(0, 4)])
        self.nodes = [node1, node2, node3]

