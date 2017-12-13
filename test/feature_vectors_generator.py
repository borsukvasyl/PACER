import random
import numpy as np


class FeatureVectorsGenerator:
    def __init__(self, n, h):
        self._number_of_nodes = n
        self._number_of_features = h
        self._feature_values = [0.0] * 3 + list(map(lambda x: round(float(x), 1),
                                                                   np.arange(0.1, 1.1, 0.1)))
        random.shuffle(self._feature_values)

    def generate_feature_vectors(self):
        features_dict = {}
        for node_index in range(self._number_of_nodes):
            features_dict[node_index] = self.generate_feature_vector()
        return features_dict

    def generate_feature_vector(self):
        feature_values = [0.0] * self._number_of_features + list(map(lambda x: round(float(x), 1),
                                                                   np.arange(0.1, 1.1, 0.1)))
        random.shuffle(feature_values)

        feature_vector = []
        number_of_zeros = self._number_of_features
        for feature_index in range(self._number_of_features):
            feature_value = random.choice(feature_values)
            if feature_value != 0.0:
                feature_values += [0.0] * number_of_zeros
                number_of_zeros *= 2
            feature_vector.append(feature_value)
        return tuple(feature_vector)


if __name__ == "__main__":
    fvg = FeatureVectorsGenerator(6, 4)
    res = fvg.generate_feature_vectors()
    print(res)
