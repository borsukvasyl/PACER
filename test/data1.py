VQ = [0, 1, 2, 3, 5]
# FIQ = {0: [(2, 1), (1, 0.7)],
#        1: [(0, 1), (3, 0.8)]}
FIQ = {0: {2: 1, 1: 0.7},
       1: {0: 1, 3: 0.8}}
HIQ = {0: {0: 0, 1: 12, 5: 12},
       1: {1: 0, 5: 4, 2: 5},
       2: {2: 0, 3: 4, 5: 5},
       3: {3: 0, 5: 3},
       5: {5: 0}}


if __name__ == "__main__":
    from compact_states.compact_states import CompactStates
    from compact_states.compact_state import CompactState
    from compact_states.route import Route
    from compact_states.nodes_set import NodesSet

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

    import pacer
    import user_query
    pc = pacer.PACER(user_query.Query(1, 5, 13), VQ, FIQ, HIQ)
    print(pc.pruning1(css, NodesSet({1, 2, 5}), 3).route)
