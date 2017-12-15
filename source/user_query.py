class Query:
    """
    Class for containing user query.
    """
    def __init__(self, start, finish, budget,
                 preference=tuple(0.5 for _ in range(3)), teta=tuple(0 for _ in range(3)),
                 alpha=1):
        """
        Query initialization.
        :param start: start point
        :param finish: end point
        :param budget: travel budget
        :param preference: feature preference vector
        :param teta: feature filtering vector
        :param alpha: alpha
        """
        self._query = [start, finish, budget, preference, teta, alpha]

    def get_start(self):
        """
        Gets start point.
        :return: start point
        """
        return self._query[0]

    def get_finish(self):
        """
        Gets end point.
        :return: end point
        """
        return self._query[1]

    def get_budget(self):
        """
        Gets travel budget.
        :return: budget
        """
        return self._query[2]

    def get_preference(self):
        """
        Gets feature preference vector.
        :return: feature preference
        """
        return self._query[3]

    def get_teta(self):
        """
        Gets feature filtering vector.
        :return: filtering vector
        """
        return self._query[4]

    def get_alpha(self):
        """
        Gets alpha.
        :return: alpha
        """
        return self._query[5]
