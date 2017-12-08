class FeatureIndex:
    class NodeFeatureValue:
        def __init__(self, i, v):
            self._node = i
            self._feature_value = v

        def __repr__(self):
            return "NodeFV({0}, {1})".format(self.get_node(), self.get_value())

        def get_node(self):
            return self._node

        def get_value(self):
            return self._feature_value

    def __init__(self, n):
        self.number_of_features = n
        self._features = dict([(i, []) for i in range(n)])

    def get_fi(self):
        return self._features

    def add_element(self, feature, element):
        """

        :param feature: index
        :param element: tuple:(node_index, feature_value)
        :return:
        """
        if feature not in self._features:
            raise KeyError("Invalid feature")

        fi_element = FeatureIndex.NodeFeatureValue(element[0], element[1])
        self._features.get(feature).append(fi_element)
        self._features.get(feature).sort(key=lambda x: x.get_value(), reverse=True)

    def remove_element(self, feature, element):
        """

        :param feature: index
        :param element: tuple:(node_index, feature_value)
        :return:
        """
        if feature not in self._features:
            raise KeyError("Invalid feature")

        self._features.get(feature).remove(element)

    def cut(self, start, finish, feature_vector, filtering_vector):
        """
        Reduces feature index(FI) to FIQ due to user query
        :param start: index of start poi
        :param finish: index of finish poi
        :param feature_vector: tuple of features' ratings preferences
        :param filtering_vector: tuple of filtering(pois with lower ratings will be cut off)
        :return:
        """
        # remove useless features
        query_features = list(filter(lambda x: feature_vector[x] > 0, self._features.keys()))
        query_features_dict = dict(zip(query_features,
                                       [self._features.get(f) for f in query_features]))
        self._set_features(query_features_dict)

        # remove useless nodes in each feature
        features_to_delete = set()
        index = 0
        for feature in self._features:
            feature_filter_value = filtering_vector[index]
            query_nodes = list(filter(lambda node: (node.get_node() == start) or
                                                   (node.get_node() == finish) or
                                                   (node.get_value() > feature_filter_value),
                                      self._features[feature]
                                      )
                               )
            if query_nodes:
                self._features[feature] = query_nodes
            else:
                features_to_delete.add(feature)
            index += 1

        # remove useless features
        for feature in features_to_delete:
            del (self._features[feature])

    def _set_features(self, features):
        """
        Set features attribute to given value
        :param features: dict of features
        :return:
        """
        self._features = features


if __name__ == "__main__":
    fi = FeatureIndex(3)
    fi.add_element(0, (1, 0.6))
    fi.add_element(1, (2, 0.1))
    fi.add_element(2, (3, 1.0))
    print(fi.get_fi())
    fi.cut(0, 5, (0.6, 0.1, 0.5), (0.5, 0, 0.5))
    print(fi.get_fi())
