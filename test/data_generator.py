import shutil
import os
import random
from test.adjacency_matrix import AdjacencyMatrix
from test.feature_vectors_generator import FeatureVectorsGenerator


class DataGenerator:
    """
    Generate input data: adjacency matrix, list of feature vectors, user query for K graphs
    """
    # Bounds:
    # Number of nodes
    N = (5, 20)
    # Number of features
    H = (2, 10)

    def __init__(self, k):
        self._number_of_cases = k

    def generate(self):
        # remove previous folder of data and create new
        DATA_FOLDER = "data/"
        base_dir = os.getcwd()
        shutil.rmtree(base_dir + "/" + DATA_FOLDER, ignore_errors=True)
        os.mkdir(DATA_FOLDER)
        os.chdir(os.getcwd() + "/" + DATA_FOLDER)

        for i in range(self._number_of_cases):
            # generate graph
            number_of_nodes = random.randint(DataGenerator.N[0], DataGenerator.N[1])
            matrix = AdjacencyMatrix(number_of_nodes)
            graph = matrix.generate_random()

            # generate list of feature vectors
            number_of_features = random.randint(DataGenerator.H[0], DataGenerator.H[1])
            features_generator = FeatureVectorsGenerator(number_of_nodes, number_of_features)
            feature_vectors = features_generator.generate_feature_vectors()
            DataGenerator.write_data(str(i), graph, feature_vectors)

    @staticmethod
    def write_data(filename, matrix, list_of_vectors):
        with open("data" + filename, 'w') as file:
            file.write(str(matrix) + '\n')
            file.write(str(list_of_vectors))


if __name__ == "__main__":
    data_gen = DataGenerator(2)
    data_gen.generate()