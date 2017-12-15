import random


class AdjacencyMatrix:
    MAX_COST = 100

    def __init__(self, n, matrix=None):
        """
        :param n: number of nodes
        """
        self._size = n
        if matrix is None:
            self._matrix = [[] for _ in range(n - 1)]
        else:
            self._matrix = matrix

    def __len__(self):
        return self._size

    def get_value(self, i, j):
        if i < 0 or i >= self._size or j < 0 or j >= self._size:
            raise IndexError("Matrix does not have such elements")

        if i == j:
            return 0
        elif j < i:
            i, j = j, i

        try:
            return self._matrix[i][j - i - 1]
        except IndexError:
            print("You are doing smth wrong")

    def generate_random(self, is_complete=True):
        for i in range(self._size):
            for _ in range(i + 1, self._size):
                random_cost = random.randrange(1, AdjacencyMatrix.MAX_COST)
                if is_complete:
                    self._matrix[i].append(random_cost)
                else:
                    self._matrix[i].append(random_cost if random.randrange(0, 3) else 0)
        return self._matrix


if __name__ == "__main__":
    n = 5
    matrix = AdjacencyMatrix(n)
    matrix.generate_random()
    print("M[0][0]", matrix.get_value(0, 0))
    print("M[1][3]", matrix.get_value(1,3))
    print("M[3][1]", matrix.get_value(3,1))
    print("M[1][4]", matrix.get_value(1,4))
