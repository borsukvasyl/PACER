"""
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

G.add_edge('a', 'b', weight=0.6)
G.add_edge('a', 'c', weight=0.2)
G.add_edge('c', 'd', weight=0.1)
G.add_edge('c', 'e', weight=0.7)
G.add_edge('c', 'f', weight=0.9)
G.add_edge('a', 'd', weight=0.3)

pos = nx.spring_layout(G)  # positions for all nodes
#################################################################################
route = ["a", "c", "d"]

route_edges = [(u, v) for (u, v, d) in G.edges(data=True) if u in route and v in route]
edges = [(u, v) for (u, v, d) in G.edges(data=True) if (u, v) not in route_edges]

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, edgelist=edges, width=6)
nx.draw_networkx_edges(G, pos, edgelist=route_edges, width=6, alpha=0.5, edge_color='b', style='dashed')

# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

print(pos)
plt.axis('off')
plt.savefig("route1.png")  # save as png
plt.show()  # display
#################################################################################
route = ["e", "c", "f"]

route_edges = [(u, v) for (u, v, d) in G.edges(data=True) if u in route and v in route]
edges = [(u, v) for (u, v, d) in G.edges(data=True) if (u, v) not in route_edges]

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, edgelist=edges, width=6)
nx.draw_networkx_edges(G, pos, edgelist=route_edges, width=6, alpha=0.5, edge_color='b', style='dashed')

# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

print(pos)
plt.axis('off')
plt.savefig("route2.png")  # save as png
plt.show()  # display
"""
import matplotlib.pyplot as plt
import networkx as nx


class GraphDrawer(object):
    @staticmethod
    def draw_routes(adjacency_matrix, routes, filename=None):
        graph = GraphDrawer.initialize_graph(adjacency_matrix)


    @staticmethod
    def initialize_graph(adjacency_matrix):
        graph = nx.Graph()
        return graph

    @staticmethod
    def draw_route(graph, route, filename=None):
        pass


if __name__ == "__main__":
    from source.preindexing_with_adj_matrix.indexator import Indexator
    from source.user_query import Query
    from source.pacer import PACER
    from test.adjacency_matrix import AdjacencyMatrix

    am = [[32, 93, 47, 24, 55],
               [5, 87, 11, 64],
                   [41, 6, 19],
                      [37, 80],
                          [29]]
    fi = {0: (0.4, 0.7, 0.0, 0.5), 1: (0.0, 0.3, 0.0, 0.0), 2: (0.0, 0.0, 0.5, 0.0),
          3: (0.0, 0.7, 0.5, 0.1), 4: (1.0, 0.0, 0.1, 0.0), 5: (0.0, 0.6, 0.8, 0.0)}

    query = Query(0, 3, 120, preference=tuple(0.5 for _ in range(4)),
                  teta=tuple(0 for _ in range(4)))

    ind = Indexator(fi, AdjacencyMatrix(5, matrix=am), query)

    FIQ, VQ = ind.find_fiq_and_vq()
    HIQ = ind.find_hiq(VQ)

    pc = PACER(query, VQ, FIQ, HIQ)
    pq = pc.find_topk_routes()
    routes = [pq.delete() for _ in range(pq.size())]
    print(routes)

    GraphDrawer.draw_routes(am, routes)
