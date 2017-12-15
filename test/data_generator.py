import shutil
import os
import random
import numpy as np
from test.adjacency_matrix import AdjacencyMatrix
from test.feature_vectors_generator import FeatureVectorsGenerator


class DataGenerator:
    """
    Generate input data: adjacency matrix, list of feature vectors, user query for K graphs
    """
    # Bounds:
    # Number of nodes
    N = (5, 8)
    # Number of features
    H = (2, 4)

    @staticmethod
    def generate(number_of_cases, is_complete=True):
        # remove previous folder of data and create new
        DATA_FOLDER = "data/"
        base_dir = os.getcwd()
        shutil.rmtree(base_dir + "/" + DATA_FOLDER, ignore_errors=True)
        os.mkdir(DATA_FOLDER)

        for i in range(number_of_cases):
            # generate graph
            number_of_nodes = random.randint(DataGenerator.N[0], DataGenerator.N[1])
            matrix = AdjacencyMatrix(number_of_nodes)
            graph = matrix.generate_random(is_complete=is_complete)

            # generate list of feature vectors
            number_of_features = random.randint(DataGenerator.H[0], DataGenerator.H[1])
            features_generator = FeatureVectorsGenerator(number_of_nodes, number_of_features)
            feature_vectors = features_generator.generate_feature_vectors()

            # generate user query
            nodes_list = list(range(number_of_nodes))
            x = random.choice(nodes_list)
            y = random.choice(list(set(nodes_list).difference({x})))
            edge_number = (number_of_nodes * (number_of_nodes - 1)) // 2
            budget = random.randint(edge_number * 5, edge_number * 20)
            user_preference_vector = tuple([random.choice(list(map(lambda x: round(float(x), 1),
                                                             np.arange(0.0, 1.1, 0.1))))
                                      for _ in range(number_of_features)])
            filtering_vector = tuple([random.choice(list(map(lambda x: round(float(x), 1),
                                                       np.arange(0.0, 0.6, 0.1))))
                                for _ in range(number_of_features)])
            ALPHA = 1
            query = [x, y, budget, user_preference_vector, filtering_vector, ALPHA]

            DataGenerator.write_data(str(i), number_of_nodes, number_of_features, graph, feature_vectors, query)

    @staticmethod
    def write_data(filename, nodes_number, features_number, matrix, list_of_vectors, query):
        with open("data/case" + filename, 'w') as file:
            file.write(str(nodes_number) + " " + str(features_number) + '\n')
            file.write(str(matrix) + '\n')
            file.write(str(list_of_vectors) + '\n')
            file.write(str(query))


if __name__ == "__main__":
    DataGenerator.generate(2)
