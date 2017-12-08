if __name__ == "__main__":
    from source.graph.route import Route
    from source.pacer import PACER
    from source import Query
    import data1 as d1

    route = Route([1], 1)
    route1 = route.extend_route(d1.HIQ, 2)
    route2 = route.extend_route(d1.HIQ, 5)

    Q = Query(5, 1, 13)
    pacer_object = PACER(Q, d1.VQ, d1.FIQ, d1.HIQ)
    UP = pacer_object.pruning2(route1)
    print("UP=", UP)
    route1_gain = pacer_object.find_gain(set(route1.route))
    print("route1 gain =", route1_gain)
    print(route1_gain + UP)
