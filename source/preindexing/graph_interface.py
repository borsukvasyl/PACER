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
            self.node_index = i
            self.feature_vector = fv
            self.neighbours = lst

        def get_feature_vector(self):
            return self.feature_vector

        def get_neighbours(self):
            return self.neighbours


    def __init__(self):
        self.nodes = []
        # self._build_graph() TODO: write this function

    def get_nodes(self):
        for node in self.nodes:
            yield node

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

