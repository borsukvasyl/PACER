class HopIndex:
    """
    The same approach as for Feature Index
    Keeps dict of nodes indices as keys and adjacent nodes and cost to them
    as values
    IN: list of integers corresponding to indexes of nodes
    (they are retrieved by FeatureIndex.find_valid_nodes() method)
    OUT: dict:
    keys: nodes indexes,
    values: dict(key: node index, value: cost to this node)
    """
    class NodeCost:
        def __init__(self, i, d):
            self._node = i
            self._cost = d

        def __repr__(self):
            return "NodeD({0}, {1})".format(self.get_node(), self.get_cost())

        def get_node(self):
            return self._node

        def get_cost(self):
            return self._cost

    def __init__(self, nodes):
        self._nodes = dict(zip(nodes, [[] for _ in range(len(nodes))]))

    def add_element(self, node, element):
        """
        :param node: node index
        :param element: tuple:(node_index, distance(cost))
        :return:
        """
        if node not in self._nodes:
            raise KeyError("No node with such index")

        hi_element = HopIndex.NodeCost(element[0], element[1])
        self._nodes.get(node).append(hi_element)
        self._nodes.get(node).sort(key=lambda node: node.get_cost())

    def get_hi(self, budget):
        hiq = {}
        for node in self._nodes:
            for element in self._nodes[node]:
                if element.get_cost() <= budget:
                    if not hiq.get(node):
                        hiq[node] = {}
                    hiq[node][element.get_node()] = element.get_cost()

        return hiq


if __name__ == "__main__":
    from source.preindexing_with_classes.feature_index import FeatureIndex
    fi = FeatureIndex(3)
    fi.add_element(0, (1, 0.6))
    fi.add_element(1, (2, 0.1))
    fi.add_element(2, (3, 1.0))
    hi = HopIndex(fi.find_valid_nodes(0, 5, (0.6, 0.1, 0.5), (0.5, 0, 0.5)))
    hi.add_element(1, (2, 12))
    hi.add_element(1, (3, 15))
    hi.add_element(2, (3, 10))
    print(hi.get_hi(13))
