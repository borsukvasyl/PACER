class Indexator:
    def __init__(self, lst, matrix, query):
        """

        :param lst: dict(k: index, v: feature_vector)
        :param matrix: class AdjacencyMatrix
        """
        self.list_of_node_features = lst
        self.adjacency_matrix = matrix
        self._query = query

    def find_fiq_and_vq(self):
        start = self._query.get_start()
        finish = self._query.get_finish()
        feature_vector = self._query.get_preference()
        filtering_vector = self._query.get_teta()

        fiq = {}
        vq = set()
        for node in self.list_of_node_features:
            for feature_index in range(len(self.list_of_node_features[node])):
                # Check the following conditions:
                # 1. Feature value of node at position h equals zero
                # 2. Feature value of node at position h is less than feature value in filtering vector
                # at position h
                # 3. node is node a start or finish node
                # If 3rd condition and either 1 or 2 do not add node to FIQ
                if (self.list_of_node_features.get(node)[feature_index] == 0 or
                        self.list_of_node_features.get(node)[feature_index] < filtering_vector[feature_index])\
                        and (node != start and node != finish):
                    continue

                # Add node to FIQ and VQ
                if fiq.get(feature_index):
                    element = (node, self.list_of_node_features.get(node)[feature_index])
                    fiq.get(feature_index).append(element)
                else:
                    fiq[feature_index] = [(node, self.list_of_node_features.get(node)[feature_index])]
                vq.add(node)

        # remove features with zero values in feature vector
        for feature_index in range(len(feature_vector)):
            if feature_vector[feature_index] == 0:
                del(fiq[feature_index])

        return fiq, vq

    def find_hiq(self, vq, budget):
        hiq = dict.fromkeys(vq)
        for key in hiq:
            hiq[key] = {}

        for node_index in range(len(self.adjacency_matrix)):
            if node_index in vq:
                hiq.get(node_index)[node_index] = 0
                for adjacent_node_index in range(node_index + 1, len(self.adjacency_matrix)):
                    if adjacent_node_index in vq:
                        cost = self.adjacency_matrix.get_value(node_index, adjacent_node_index)
                        if cost <= budget:
                            hiq.get(node_index)[adjacent_node_index] = cost
        return hiq


if __name__ == "__main__":
    from test.adjacency_matrix import AdjacencyMatrix
    from source.user_query import Query

    n = 6
    matrix = AdjacencyMatrix(n)
    matrix.generate_random()
    query = Query(0, 2, 3, (0.5, 0.5, 0.5), (0.6, 0.6, 0.6))
    featute_dict = {0: (0.1, 0.0, 0.9),
                    1: (0.5, 0.6, 1.0),
                    2: (0.3, 0.4, 0.8),
                    3: (0.7, 0.0, 0.0),
                    4: (0.0, 0.2, 0.7),
                    5: (0.0, 0.1, 0.0),}
    indexator = Indexator(featute_dict, matrix, query)
    FIQ, VQ = indexator.find_fiq_and_vq()
    budget = 65
    HIQ = indexator.find_hiq(VQ, budget)
    print(HIQ)
