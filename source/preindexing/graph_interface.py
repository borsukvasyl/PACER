class GraphInterface:
    """
    Created to simplify manipulations with possibly unfamiliar graph
    """
    class Node:
        def __init__(self, i, fv, lst):
            """

            :param i: integer index of node
            :param fv: tuple, feature vector
            :param lst: list(tuple), list of neighbours
            """
            self._node_index = i
            self._feature_vector = fv
            self._neighbours = lst

        def get_index(self):
            return self._node_index

        def get_feature_vector(self):
            return self._feature_vector

        def get_neighbours(self):
            return self._neighbours


    def __init__(self, feature_number):
        self.nodes = []
        self._feature_number = feature_number
        # self._build_graph() TODO: write this function

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

    def _build_graph(self, graph):
        """
        #TODO: WRITE USE IGRAPH LIBRARY http://igraph.org/python/doc/igraph.GraphBase-class.html
        Build graph interface from graph from other library
        :param graph: some object of graph from foreign library
        :return:
        """
        pass

