import matplotlib.pyplot as plt
import networkx as nx


class GraphDrawer(object):
    """
    Class for visualizing graph and routes in it.
    """
    @staticmethod
    def draw_routes(adjacency_matrix, routes, graph_description, foldername=None):
        """
        Draws graph and routes in it
        :param adjacency_matrix: adjacency matrix representation of graph
        :param routes: list of tuple(route, gain)
        :param graph_description: text to add under graph plot
        :param foldername: where to save plots
        :return: None
        """
        graph = GraphDrawer.initialize_graph(adjacency_matrix)
        positions = nx.spring_layout(graph, iterations=50)

        GraphDrawer.draw_graph(graph, positions, graph_description, filename="{}/graph.png".format(foldername))

        for i in range(len(routes)):
            route_filename = None
            if foldername:
                route_filename = "{}/route{}.png".format(foldername, i + 1)
            GraphDrawer.draw_route(graph, positions, routes[i], filename=route_filename)

    @staticmethod
    def initialize_graph(adjacency_matrix):
        """
        networkx.Graph object initialization for given adjacency matrix.
        :param adjacency_matrix: adjacency matrix
        :return: Graph object
        """
        graph = nx.Graph()
        for i in range(len(adjacency_matrix)):
            for j in range(len(adjacency_matrix) - i):
                if adjacency_matrix[i][j]:
                    graph.add_edge(i, i + j + 1, weight=adjacency_matrix[i][j])
        return graph

    @staticmethod
    def draw_graph(graph, positions, graph_description, filename=None):
        """
        Draws graph.
        :param graph: Graph object
        :param positions: nodes positions
        :param graph_description: plot description
        :param filename: where to save plot
        :return: None
        """
        # nodes
        nx.draw_networkx_nodes(graph, positions, nodelist=graph.nodes(),
                               node_size=400, node_color='r')

        # edges
        edges = [(u, v) for (u, v, d) in graph.edges(data=True)]
        nx.draw_networkx_edges(graph, positions, edgelist=edges, width=1)

        # labels
        nx.draw_networkx_labels(graph, positions, font_size=10, font_family='sans-serif')
        nx.draw_networkx_edge_labels(graph, positions, font_size=8, edge_labels=nx.get_edge_attributes(graph, "weight"))

        plt.figtext(.02, .02, graph_description)
        plt.axis('off')
        if filename:
            plt.savefig(filename)  # save as png
        plt.show()  # display

    @staticmethod
    def draw_route(graph, positions, route, filename=None):
        """
        Draws routes for given graph.
        :param graph: Graph object
        :param positions: nodes positions
        :param route: tuple(route, gain)
        :param filename: where to save plot
        :return: None
        """
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
