from source.preindexing.graph_interface import GraphInterface
from source.preindexing.feature_index import FeatureIndex
from source.preindexing.hop_index import HopIndex

class Indexator:
    """
    Creates feature and hop indices from given graph
    IN: GraphInterface object
    OUT: FIQ, HIQ, VQ
    """
    def __init__(self, graph):
        self.graph = graph
        self.FI = FeatureIndex()
        self.HI = HopIndex()

    def make_indexing(self):
        for node in self.graph.get_nodes():
            pass