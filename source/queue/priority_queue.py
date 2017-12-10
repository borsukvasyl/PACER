class PriorityQueue:
    def __init__(self):
        """
        elements: list(tuple)
        tuple: data, rank
        """
        self.elements = []

    def size(self):
        return len(self.elements)

    def put(self, element):
        """
        :param element: tuple(data, rank)
        :return:
        """
        self.elements.append(element)
        self._max_heapify()

    def get(self):
        return self.elements[0]

    def get_by_index_priority(self, index):
        return self.elements[index]

    def delete(self):
        return self.elements.pop(0)

    def _max_heapify(self):
        current = len(self.elements) - 1
        while self.elements[current][1] > self.elements[self._parent(current)][1]:
            self.elements[current], self.elements[self._parent(current)] = \
                self.elements[self._parent(current)], self.elements[current]
            current = self._parent(current)

    @staticmethod
    def _left(x):
        return 2 * x + 1

    @staticmethod
    def _right(x):
        return 2 * x + 2

    @staticmethod
    def _parent(x):
        return x // 2


if __name__ == "__main__":
    pq = PriorityQueue()
    element = (3, 0)
    pq.put(element)
    element1 = (2, 1)
    pq.put(element1)
    print(pq.get())
    element2 = (1, 2)
    pq.put(element2)
    print(pq.get())
