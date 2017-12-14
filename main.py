import os
import shutil

from test.data_generator import DataGenerator
from source.preindexing_with_adj_matrix.indexator import Indexator
from test.adjacency_matrix import AdjacencyMatrix
from source.pacer import PACER
from source.user_query import Query

from source.visualization.graph_drawer import GraphDrawer


class Main:
    """
    Read data, run PACER
    """
    @staticmethod
    def main():
        # generate_data
        NUMBER_OF_TESTCASES = 3
        NUMBER_OF_ROUTES = 3
        DataGenerator.generate(NUMBER_OF_TESTCASES)

        shutil.rmtree("result" + "/", ignore_errors=True)
        os.mkdir("result")

        # find and visualize topK routes
        data_dir = os.listdir(os.getcwd() + "/data")
        for data_file in data_dir:
            node_number, features_number, graph_matrix, features_dict, query = Main.read_data("data/" + data_file)

            Q = Query(*query)

            indexator = Indexator(features_dict, AdjacencyMatrix(len(graph_matrix) + 1, graph_matrix), Q)
            FIQ, VQ = indexator.find_fiq_and_vq()
            HIQ = indexator.find_hiq(VQ)

            pacer = PACER(Q, VQ, FIQ, HIQ)
            topK = pacer.find_topk_routes()

            pq_routes = [topK.delete() for _ in range(topK.size())][:NUMBER_OF_ROUTES]
            routes = [(pq_route[0].extend_route(HIQ, Q.get_finish()), pq_route[1]) for pq_route in pq_routes]
            print(routes)

            os.mkdir("result/{}".format(data_file))
            GraphDrawer.draw_routes(graph_matrix, filename="result/route")

    @staticmethod
    def read_data(filename):
        with open(filename) as file:
            content = file.readlines()
            node_number, features_number = tuple(map(int, content[0].split()))
            graph_matrix = eval(content[1])
            features_dict = eval(content[2])
            query = eval(content[3])
        return node_number, features_number, graph_matrix, features_dict, query


if __name__ == "__main__":
    Main.main()
