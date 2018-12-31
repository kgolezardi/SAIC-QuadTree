import random

from divisions import Division


class OnlineDivision(Division):
    """
    Online Division:
    On each grid decides to divide or not, then does the same for its children (if divided).
    Note that the division probability decreases when we go deeper into grids.
    """

    DIVIDE_ITERATIONS = 400
    MAX_DIVIDE_DEPTH = 6
    PURE_DIVIDE_RATE = 0.85

    @classmethod
    def divide(cls, quadtree, depth=0):
        x = random.random()
        no_divide_prob = (cls.PURE_DIVIDE_RATE / cls.MAX_DIVIDE_DEPTH ** 2) * depth ** 2 + (1 - cls.PURE_DIVIDE_RATE)
        # print("No div prob for depth %s = %s" % (depth, no_divide_prob))
        if x > no_divide_prob:
            quadtree.divide()
            for i in range(4):
                cls.divide(quadtree.subgrids[i], depth + 1)
