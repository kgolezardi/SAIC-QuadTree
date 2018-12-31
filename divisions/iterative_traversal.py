import random

from divisions import Division


class InterativeTraversalDivision(Division):
    """
    Iterative Traversal Divison:
    On each call, it traverse randomly on the grid tree and devides when reaches a leaf.
    """

    DIVIDE_ITERATIONS = 400
    MAX_DIVIDE_DEPTH = 6

    @classmethod
    def divide(cls, quadtree):
        for i in range(cls.DIVIDE_ITERATIONS):
            cls.iterative_divide(quadtree)

    @classmethod
    def iterative_divide(cls, qt, depth=0):
        if len(qt.subgrids) == 0:
            qt.devide()
            return True
        if depth > cls.MAX_DIVIDE_DEPTH:
            return False
        devided = False
        tries = 0
        while not devided and tries < 5:
            x = random.randint(0, 3)
            devided = cls.iterative_divide(qt.subgrids[x], depth + 1)
            tries += 1
        if devided:
            return True
        return False
