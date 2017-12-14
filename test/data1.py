VQ = {0, 1, 2, 3, 5}
FIQ = {0: [(2, 1), (1, 0.7)],
       1: [(0, 1), (3, 0.8)]}
HIQ = {0: {0: 0, 1: 12, 5: 12},
       1: {1: 0, 5: 4, 2: 5},
       2: {2: 0, 3: 4, 5: 5},
       3: {3: 0, 5: 3},
       5: {5: 0}}


if __name__ == "__main__":
    from source import user_query, pacer

    pc = pacer.PACER(user_query.Query(0, 3, 27), VQ, FIQ, HIQ)
    pq = pc.find_topk_routes()

    # a = pc.compact_states._compact_states
    # for i in a:
    #     print(">>>>>>>node {}: {}".format(i, a[i].routes))

    top_routes = [pq.delete() for _ in range(pq.size())]
    print(top_routes)
