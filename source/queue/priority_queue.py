class PriorityQueue:
    def __init__(self):
        """
        PriorityQueue default initialization.
        """
        self.elements = []

    def size(self):
        """
        Calculates size of PriorityQueue.
        :return: size
        """
        return len(self.elements)

    def put(self, element):
        """
        Puts element to PriorityQueue.
        :param element: tuple(data, rank)
        :return: None
        """
        self.elements.append(element)
        self._upper_max_heapify()

    def get(self):
        """
        Gets top element from PriorityQueue.
        :return: top element
        """
        return self.elements[0]

    def delete(self):
        """
        Removes top element from PriorityQueue and returns it.
        :return: tuple(top element, priority)
        """
        removed = self.elements[0]
        self.elements[0] = self.elements[-1]
        self.elements.pop()
        self._max_heapify(0)
        return removed

    def _max_heapify(self, i):
        """
        Max heapify PriorityQueue.
        :param i: current node index
        :return: None
        """
        l = self._left(i)
        r = self._right(i)
        swap_with = i
        if l < self.size() and self.elements[l][1] > self.elements[i][1]:
            swap_with = l
        if r < self.size() and self.elements[r][1] > self.elements[i][1]:
            swap_with = r
        if swap_with != i:
            self.elements[i], self.elements[swap_with] = self.elements[swap_with], self.elements[i]
            self._max_heapify(swap_with)

    def _upper_max_heapify(self):
        """
        Upper max heapify PriorityQueue.
        :return: None
        """
        current = len(self.elements) - 1
        while self.elements[current][1] > self.elements[self._parent(current)][1]:
            self.elements[current], self.elements[self._parent(current)] = \
                self.elements[self._parent(current)], self.elements[current]
            current = self._parent(current)

    def get_by_index_priority(self, index):
        """
        Gets priority of index element.
        :param index: index position
        :return: priority
        """
        return self.elements[index]

    @staticmethod
    def _left(x):
        """
        Calculates index of left child node for x index.
        :param x: index of node
        :return: node's left child index
        """
        return 2 * x + 1

    @staticmethod
    def _right(x):
        """
        Calculates index of right child node for x index.
        :param x: index of node
        :return: node's right child index
        """
        return 2 * x + 2

    @staticmethod
    def _parent(x):
        """
        Calculates index of parent node for x index.
        :param x: index of node
        :return: node's parent index
        """
        return x // 2


if __name__ == "__main__":
    pq = PriorityQueue()
    pq.put((3, 0))
    pq.put((2, 1))
    pq.put((1, 2))
    pq.put((3, 7))
    pq.put((3, 4))
    pq.put((3, 2))
    print(pq.elements)
    print(pq.delete())
    print(pq.elements)
    print(pq.delete())
    print(pq.elements)
    print(pq.delete())
    print(pq.elements)
    print(pq.delete())
    print(pq.elements)
