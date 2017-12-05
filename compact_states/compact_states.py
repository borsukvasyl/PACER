class CompactStates(object):
    def __init__(self):
        """
        Initialize compact states dictionary
        """
        self.compact_states = {}

    def add_compact_state(self, points, compact_state):
        """
        Adds points: compact_state to compact states dictionary.
        :param points: compact state's points set
        :param compact_state: CompactState object
        :return: None
        """
        self.compact_states[str(points)] = compact_state

    def get_compact_state(self, points):
        """
        Returns compact state of points set.
        :param points: compact state's points set
        :return: CompactState
        """
        return self.compact_states[str(points)]
