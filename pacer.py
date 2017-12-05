class PACER(object):
    def __init__(self, Q, VQ, FIQ, HIQ):
        """
        Initializing PACER.
        :param Q: tuple(x, y, b, w, O, F)
        :param VQ: POI candidates
        :param FIQ: Feature Index
        :param HIQ: 2-Hop Index
        """
        self.Q = Q
        self.VQ = VQ
        self.FIQ = FIQ
        self.HIQ = HIQ
        #self.topk = PriorityQueue()

    def find_topk_routes(self):
        """
        Finds topk routes.
        :return: ---
        """
        # recursive call of _find_topk_routes
        pass

    def _find_topk_routes(self):
        """
        Finds topk routes.
        :return: ---
        """

    def find_gain(self, points):
        """
        Computes gain of given POIs.
        :param points: set of POIs
        :return: ---
        """
        pass

    def find_cost(self, route):
        """
        Computes cost of given route.
        :param route: Route object
        :return: ---
        """
        pass

    def pruning1(self, points, point):
        """
        PACER's pruning-1.
        :param points: set of POIs
        :param point: current POI
        :return: ---
        """
        pass

    def pruning2(self):
        pass
