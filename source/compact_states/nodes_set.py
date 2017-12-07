class NodesSet(set):
    """
    Common set, but is hashable.
    """
    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        return super(NodesSet, self).__repr__()

    def get_prefix(self, element):
        result = NodesSet()
        for val in self:
            if val < element:
                result.add(val)
        return result