import matplotlib.pyplot as plt
import networkx as nx


class GraphDrawer(object):
    @staticmethod
    def draw_routes(adjacency_matrix, routes, filename=None):
        graph = GraphDrawer.initialize_graph(adjacency_matrix)
        positions = nx.spring_layout(graph, iterations=50)
        for i in range(len(routes)):
            route_filename = None
            if filename:
                route_filename = "{}{}.png".format(filename, i + 1)
            GraphDrawer.draw_route(graph, positions, routes[i], filename=route_filename)

    @staticmethod
    def initialize_graph(adjacency_matrix):
        graph = nx.Graph()
        for i in range(len(adjacency_matrix)):
            for j in range(len(adjacency_matrix) - i):
                graph.add_edge(i, i + j + 1, weight=adjacency_matrix[i][j])
        return graph

    @staticmethod
    def draw_route(graph, positions, route, filename=None):
        # nodes
        blue_nodes = [route[0].get_first_node(), route[0].get_last_node()]
        red_nodes = [node for node in graph.nodes() if node not in blue_nodes]
        print(blue_nodes, red_nodes)
        nx.draw_networkx_nodes(graph, positions, nodelist=blue_nodes,
                               node_size=400, node_color='b')
        nx.draw_networkx_nodes(graph, positions, nodelist=red_nodes,
                               node_size=400, node_color='r')

        # edges
        route_edges = [(route[0].route[i], route[0].route[i + 1]) for i in range(len(route[0].route) - 1)]
        edges = [(u, v) for (u, v, d) in graph.edges(data=True) if
                 not ((u, v) in route_edges or (v, u) in route_edges)]
        nx.draw_networkx_edges(graph, positions, edgelist=edges, width=1)
        nx.draw_networkx_edges(graph, positions, edgelist=route_edges, width=3,
                               alpha=0.5, edge_color='b')

        # labels
        nx.draw_networkx_labels(graph, positions, font_size=10, font_family='sans-serif')

        plt.axis('off')
        if filename:
            plt.savefig(filename)  # save as png
        plt.show()  # display

    @staticmethod
    def _check_uv_is_in_route(u, v, route):
        if u not in route[0].route:
            return False
        if v in route[0].route and route[0].route.index(v) == route[0].route.index(u) + 1:
            return True
        return False


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

    query = Query(0, 3, 79, preference=tuple(0.5 for _ in range(4)),
                  teta=tuple(0 for _ in range(4)))

    ind = Indexator(fi, AdjacencyMatrix(5, matrix=am), query)

    FIQ, VQ = ind.find_fiq_and_vq()
    HIQ = ind.find_hiq(VQ)

    pc = PACER(query, VQ, FIQ, HIQ)
    pq = pc.find_topk_routes()
    pq_routes = [pq.delete() for _ in range(pq.size())]
    routes = [(pq_route[0].extend_route(HIQ, query.get_finish()), pq_route[1]) for pq_route in pq_routes]
    print(routes)

    GraphDrawer.draw_routes(am, routes, filename="route")
