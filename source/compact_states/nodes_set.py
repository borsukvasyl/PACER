class NodesSet(set):
    """
    Common set, but is hashable.
    """
    def get_prefix(self, element):
        """
        Calculates prefix (smaller elements) of given element from NodesSet
        :param element:
        :return:
        """
        result = NodesSet()
        for val in self:
            if val < element:
                result.add(val)
        return result

    def __hash__(self):
        """
        Returns hash of NodesSet.
        :return:
        """
        return hash(tuple(self))

    def __repr__(self):
        """
        Returns string representation of CompactState
        :return: string representation
        """
        return super(NodesSet, self).__repr__()
