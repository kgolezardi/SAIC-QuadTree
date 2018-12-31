import svgwrite
import random

PAGE_SIZE = (0, 0, 700, 700)
DIVIDE_ITERATIONS = 400
MAX_DIVIDE_DEPTH = 6
PURE_DIVIDE_RATE = 0.85


class QuadTree:
    def __init__(self):
        self.subgrids = []

    def divide(self):
        for i in range(4):
            self.subgrids.append(QuadTree())


def draw_grids(dwg, grid, position):
    if len(grid.subgrids) == 0:
        return

    x1, y1, x2, y2 = position
    up = ((x1 + x2) / 2, y1)
    right = (x2, (y1 + y2) / 2)
    down = ((x1 + x2) / 2, y2)
    left = (x1, (y1 + y2) / 2)
    center = ((x1 + x2) / 2, (y1 + y2) / 2)

    dwg.add(dwg.line(up, down, stroke=svgwrite.rgb(10, 10, 16, '%')))
    dwg.add(dwg.line(left, right, stroke=svgwrite.rgb(10, 10, 16, '%')))

    draw_grids(dwg, grid.subgrids[0], (x1, y1) + center)
    draw_grids(dwg, grid.subgrids[1], up + right)
    draw_grids(dwg, grid.subgrids[2], center + (x2, y2))
    draw_grids(dwg, grid.subgrids[3], left + down)


def random_division_iterative_traversal(qt, depth=0):
    """
    Iterative Traversal Divison:
    On each call, it traverse randomly on the grid tree and devides when reaches a leaf.
    """
    if len(qt.subgrids) == 0:
        qt.devide()
        return True
    if depth > MAX_DIVIDE_DEPTH:
        return False
    devided = False
    tries = 0
    while not devided and tries < 5:
        x = random.randint(0, 3)
        devided = random_division_iterative_traversal(qt.subgrids[x], depth + 1)
        tries += 1
    if devided:
        return True
    return False


def random_division_on_the_go(qt, depth=0):
    """
    On The Go Division:
    On each grid decides to divide or not, then does the same for its children (if divided).
    Note that the division probability decreases when we go deeper into grids.
    """
    x = random.random()
    no_divide_prob = (PURE_DIVIDE_RATE / MAX_DIVIDE_DEPTH ** 2) * depth ** 2 + (1 - PURE_DIVIDE_RATE)
    print("No div prob for depth %s = %s" % (depth, no_divide_prob))
    if x > no_divide_prob:
        qt.divide()
        for i in range(4):
            random_division_on_the_go(qt.subgrids[i], depth + 1)


def random_division_uniform(qt):
    """
    Uniform Division:
    Keeps a list of all leaf grids, selects one randomly, and divides the chosen grid.
    """
    seed = [(qt, 0)]
    for i in range(DIVIDE_ITERATIONS):
        x = random.randint(0, len(seed) - 1)
        qt, depth = seed[x]
        seed.pop(x)
        qt.divide()
        depth += 1
        if depth < MAX_DIVIDE_DEPTH:
            for j in range(4):
                seed.append((qt.subgrids[j], depth))


qtree = QuadTree()
# for i in range(DEVIDE_ITERATIONS):
#     random_devide_iterative(grid)
random_division_uniform(qtree)

dwg = svgwrite.Drawing('out/test.svg', profile='tiny')
draw_grids(dwg, qtree, PAGE_SIZE)
dwg.save()
