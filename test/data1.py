VQ = {0, 1, 2, 3, 5}
# FIQ = {0: [(2, 1), (1, 0.7)],
#        1: [(0, 1), (3, 0.8)]}
FIQ = {0: [(2, 1), (1, 0.7)],
       1: [(0, 1), (3, 0.8)]}
HIQ = {0: {0: 0, 1: 12, 5: 12},
       1: {1: 0, 5: 4, 2: 5},
       2: {2: 0, 3: 4, 5: 5},
       3: {3: 0, 5: 3},
       5: {5: 0}}


if __name__ == "__main__":
    from source.compact_states.compact_states import CompactStates
    from source.compact_states.compact_state import CompactState
    from source.compact_states.nodes_set import NodesSet
    from source.graph.route import Route

    css = CompactStates()

    route = Route([1], 1)
    route1 = route.extend_route(HIQ, 2)
    route2 = route.extend_route(HIQ, 5)

    cs1 = CompactState(1)
    cs1.add_route(route1.extend_route(HIQ, 5))
    cs1.add_route(route2.extend_route(HIQ, 2))
    nodes_set1 = NodesSet({1, 2, 5})
    print(cs1.routes[0].route, cs1.routes[1].route)

    cs2 = CompactState(2)
    cs2.add_route(route1)
    nodes_set2 = NodesSet({1, 2})
    print(cs2.routes[0].route)

    css.add_compact_state(nodes_set1, cs1)
    css.add_compact_state(nodes_set2, cs2)
    print(css)

    from source import user_query, pacer

    pc = pacer.PACER(user_query.Query(1, 5, 24), VQ, FIQ, HIQ)
    pc.compact_states = css
    # print(pc.pruning1(NodesSet({1, 2, 5}), 0).route)
    # print(pc.find_gain(NodesSet({1, 2, 5})))

    pq = pc.find_topk_routes()

    a = pc.compact_states._compact_states
    for i in a:
        print(">>>>>>>node {}: {}".format(i, a[i].routes))

    top_routes = [pq.delete() for _ in range(pq.size())]
    print(top_routes)
