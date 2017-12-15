class CompactStates(object):
    def __init__(self):
        """
        Initialize compact states dictionary
        """
        self._compact_states = {}

    def add_compact_state(self, nodes, compact_state):
        """
        Adds points: compact_state to compact states dictionary.
        :param nodes: compact state's NodesSet
        :param compact_state: CompactState object
        :return: None
        """
        self._compact_states[nodes] = compact_state

    def get_compact_state(self, nodes):
        """
        Returns compact state of points set.
        :param nodes: compact state's NodesSet
        :return: CompactState
        """
        return self._compact_states[nodes]

    def __str__(self):
        """
        Returns string representation of CompactStates
        :return: string representation
        """
        return str(self._compact_states)
