class NodesSet(set):
    """
    Common set, but is hashable.
    """
    def __hash__(self):
        return hash(tuple(self))

    def get_prefix(self, element):
        result = {}
        for val in self:

