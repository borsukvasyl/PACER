import matplotlib.pyplot as plt
import networkx as nx


class GraphDrawer(object):
    @staticmethod
    def draw_routes(adjacency_matrix, routes, foldername=None):
        graph = GraphDrawer.initialize_graph(adjacency_matrix)
        positions = nx.spring_layout(graph, iterations=50)

        GraphDrawer.draw_graph(graph, positions, filename="{}/graph.png".format(foldername))

        for i in range(len(routes)):
            route_filename = None
            if foldername:
                route_filename = "{}/route{}.png".format(foldername, i + 1)
            GraphDrawer.draw_route(graph, positions, routes[i], filename=route_filename)

    @staticmethod
    def initialize_graph(adjacency_matrix):
        graph = nx.Graph()
        for i in range(len(adjacency_matrix)):
            for j in range(len(adjacency_matrix) - i):
                if adjacency_matrix[i][j]:
                    graph.add_edge(i, i + j + 1, weight=adjacency_matrix[i][j])
        return graph

    @staticmethod
    def draw_graph(graph, positions, filename=None):
        # nodes
        nx.draw_networkx_nodes(graph, positions, nodelist=graph.nodes(),
                               node_size=400, node_color='r')

        # edges
        edges = [(u, v) for (u, v, d) in graph.edges(data=True)]
        nx.draw_networkx_edges(graph, positions, edgelist=edges, width=1)

        # labels
        nx.draw_networkx_labels(graph, positions, font_size=10, font_family='sans-serif')
        nx.draw_networkx_edge_labels(graph, positions, font_size=8, edge_labels=nx.get_edge_attributes(graph, "weight"))

        plt.axis('off')
        if filename:
            plt.savefig(filename)  # save as png
        plt.show()  # display

    @staticmethod
    def draw_route(graph, positions, route, filename=None):
        # nodes
        blue_nodes = [route[0].get_first_node(), route[0].get_last_node()]
        red_nodes = [node for node in graph.nodes() if node not in blue_nodes]

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
        plt.figtext(.02, .02, "route: {}\ncost: {}\ngain: {}".format(" -> ".join(map(str, route[0].route)),
                    route[0].cost, round(route[1], 4)))
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
