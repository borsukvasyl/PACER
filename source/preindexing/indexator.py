from source.preindexing.graph_interface import GraphInterface
from source.preindexing.feature_index import FeatureIndex
from source.preindexing.hop_index import HopIndex


class Indexator:
    """
    Creates feature and hop indices from given graph
    IN: GraphInterface object
    OUT: FIQ, HIQ, VQ
    """

    def __init__(self, graph, query):
        self.graph = graph
        self.query = query

    def make_indexing(self):
        """
        :return: tuple: (VQ, FIQ, HIQ)
        """
        # Build feature index
        FI = FeatureIndex(self.graph.get_feature_number())
        for node in self.graph.get_nodes():
            feature_vector = GraphInterface.get_node_feature_vector(node)
            for h in range(len(feature_vector)):
                if feature_vector[h] != 0.0:
                    FI.add_element(h, (node.get_index(), feature_vector[h]))

        # Find valid nodes for Hop Index (VQ)
        start = self.query.get_start()
        finish = self.query.get_finish()
        user_preference = self.query.get_preference()
        filtering_vector = self.query.get_teta()
        VQ = FI.find_valid_nodes(start, finish, user_preference, filtering_vector)

        # Retrieve FIQ
        FIQ = FI.get_fi()

        # Build Hop Index
        HI = HopIndex(VQ)
        used_nodes = set()
        for node in self.graph.get_nodes():
            if GraphInterface.get_node_index(node) in VQ:
                current_node_index = GraphInterface.get_node_index(node)
                HI.add_element(current_node_index, (current_node_index, 0))
                for neighbour in GraphInterface.get_node_neighbours(node):
                    neighbour_index = GraphInterface.get_node_neighbour_index(neighbour)
                    if neighbour_index in VQ and neighbour_index not in used_nodes:
                        cost_to_node = GraphInterface.get_node_neighbour_cost(neighbour)
                        HI.add_element(GraphInterface.get_node_index(node),
                                       (neighbour_index, cost_to_node))
            used_nodes.add(GraphInterface.get_node_index(node))
        # Retrieve Hop Index HIQ
        budget = self.query.get_budget()
        HIQ = HI.get_hi(budget)

        return FIQ, HIQ, VQ


if __name__ == "__main__":
    from source.user_query import Query

    FEATURE_NUMBER = 3
    graph = GraphInterface(FEATURE_NUMBER)
    query = Query(0, 2, 3, (0.5, 0.5, 0.5), (0.6, 0.6, 0.6))
    indexator = Indexator(graph, query)
    FIQ, HIQ, VQ = indexator.make_indexing()
    print("FIQ:" , FIQ)
    print("HIQ:", HIQ)
    print("VQ:", VQ)
