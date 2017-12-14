from graph_tool.all import *


g = Graph(directed=False)
v1 = g.add_vertex()
v2 = g.add_vertex()
e = g.add_edge(v1, v2)
graph_draw(g, vertex_text=g.vertex_index, output_size=(200, 200), output="1.png")

'''
class GraphDrawer(object):
    @staticmethod
    def draw_graph(HIQ):
        vertices = ["one", "two", "three"]
        edges = [(0, 2), (2, 1), (0, 1)]

        g = Graph(vertex_attrs={"label": vertices}, edges=edges, directed=True)

        plot(g)

    @staticmethod
    def draw_route(HIQ, route):
        pass'''
