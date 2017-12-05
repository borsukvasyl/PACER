class Query:
    def __init__(self, nodes_list_len, start, finish, budget, w=tuple([0.5 for _ in range(3)]),
                 teta=0, alpha=1):
        self._query = [start, finish, budget, w,
                 teta, alpha]

    def get_start(self):
        return self._query[0]

    def get_finish(self):
        return self._query[1]

    def get_budget(self):
        return self._query[2]

    def get_w(self):
        return self._query[3]

    def get_teta(self):
        return self._query[4]

    def get_alpha(self):
        return self._query[5]
