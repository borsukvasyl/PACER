import os
import shutil

from source.pacer import PACER
from source.preindexing.adjacency_matrix import AdjacencyMatrix
from source.preindexing.indexator import Indexator
from source.user_query import Query
from source.visualization.graph_drawer import GraphDrawer
from test.data_generator import DataGenerator


class Main:
    """
    Read data, run PACER
    """
    @staticmethod
    def main(generate_data=False):
        """
        Runs PACER and displays results.
        :param generate_data: if is set to True generates new data
        :return: None
        """
        NUMBER_OF_TESTCASES = 3
        GENERATE_COMPLETE_GRAPH = True
        NUMBER_OF_ROUTES = 5

        # generate_data
        if generate_data:
            DataGenerator.generate(NUMBER_OF_TESTCASES, is_complete=GENERATE_COMPLETE_GRAPH)

        shutil.rmtree("result" + "/", ignore_errors=True)
        os.mkdir("result")

        # find and visualize topK routes
        data_dir = os.listdir(os.getcwd() + "/data")
        for data_file in data_dir:
            node_number, features_number, graph_matrix, features_dict, query = Main.read_data("data/" + data_file)
            print(graph_matrix)

            Q = Query(*query)

            indexator = Indexator(features_dict, AdjacencyMatrix(len(graph_matrix) + 1, graph_matrix), Q)
            FIQ, VQ = indexator.find_fiq_and_vq()
            HIQ = indexator.find_hiq(VQ)

            pacer = PACER(Q, VQ, FIQ, HIQ)
            topK = pacer.find_topk_routes()

            pq_routes = [topK.delete() for _ in range(topK.size())][:NUMBER_OF_ROUTES]
            routes = [(pq_route[0].extend_route(HIQ, Q.get_finish()), pq_route[1]) for pq_route in pq_routes]
            print(routes)

            description = "\n\nstart: {};  finish: {};  budget: {};  preference:  {}\n".format(query[0], query[1],
                                                                                               query[2], query[3])
            feature_lst = ["{}: {}".format(i, features_dict[i]) for i in features_dict]
            for i in range(1, len(feature_lst)+1):
                description += feature_lst[i-1]
                description += ";   " if i % 3 else "\n"

            os.mkdir("result/{}".format(data_file))
            GraphDrawer.draw_routes(graph_matrix, routes, description, foldername="result/{}".format(data_file))

    @staticmethod
    def read_data(filename):
        """
        Reads data from file.
        :param filename: filename
        :return: number of nodes, number of features, adjacency matrix, feature vectors, user query
        """
        with open(filename) as file:
            content = file.readlines()
            node_number, features_number = tuple(map(int, content[0].split()))
            graph_matrix = eval(content[1])
            features_dict = eval(content[2])
            query = eval(content[3])
        return node_number, features_number, graph_matrix, features_dict, query


if __name__ == "__main__":
    Main.main(True)
