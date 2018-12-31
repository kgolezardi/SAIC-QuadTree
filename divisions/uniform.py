import random

from divisions import Division


class UniformDivision(Division):
    """
    Uniform Division:
    Keeps a list of all leaf grids, selects one randomly, and divides the chosen grid.
    """

    DIVIDE_ITERATIONS = 400
    MAX_DIVIDE_DEPTH = 6

    @classmethod
    def divide(cls, quadtree):
        seed = [(quadtree, 0)]
        for i in range(cls.DIVIDE_ITERATIONS):
            x = random.randint(0, len(seed) - 1)
            qt, depth = seed[x]
            seed.pop(x)
            qt.divide()
            depth += 1
            if depth < cls.MAX_DIVIDE_DEPTH:
                for j in range(4):
                    seed.append((qt.subgrids[j], depth))
