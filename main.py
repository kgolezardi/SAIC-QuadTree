import svgwrite
import random

from divisions import UniformDivision
from shapes import NoShape, Circle, Rectangle, Decagon, Octagon

PAGE_SIZE = (0, 0, 700, 700)


class QuadTree:
    def __init__(self):
        self.subgrids = []
        self.shape = None

    def divide(self):
        for i in range(4):
            self.subgrids.append(QuadTree())


def draw_grids(dwg, grid, position, show_lines=True):
    if len(grid.subgrids) == 0:
        grid.shape.draw(dwg, position)
        return

    x1, y1, x2, y2 = position
    up = ((x1 + x2) / 2, y1)
    right = (x2, (y1 + y2) / 2)
    down = ((x1 + x2) / 2, y2)
    left = (x1, (y1 + y2) / 2)
    center = ((x1 + x2) / 2, (y1 + y2) / 2)

    if show_lines:
        dwg.add(dwg.line(up, down, stroke=svgwrite.rgb(10, 10, 16, '%')))
        dwg.add(dwg.line(left, right, stroke=svgwrite.rgb(10, 10, 16, '%')))

    draw_grids(dwg, grid.subgrids[0], (x1, y1) + center, show_lines)
    draw_grids(dwg, grid.subgrids[1], up + right, show_lines)
    draw_grids(dwg, grid.subgrids[2], center + (x2, y2), show_lines)
    draw_grids(dwg, grid.subgrids[3], left + down, show_lines)


def generate_grids(quadtree, algorithm):
    algorithm.divide(quadtree)


def assign_shapes(quadtree):
    if len(quadtree.subgrids) == 0:
        prob_sum = 0
        cutoff = []
        for shape, prob in shapes:
            cutoff.append(prob_sum)
            prob_sum += prob
        x = random.random() * prob_sum
        for i in range(len(shapes)):
            if cutoff[i] > x:
                break
            quadtree.shape = shapes[i][0]
    else:
        for qt in quadtree.subgrids:
            assign_shapes(qt)


shapes = [
    (NoShape, 12),
    (Circle, 2),
    (Rectangle, 4),
    (Decagon, 2),
    (Octagon, 2),
]

qtree = QuadTree()
generate_grids(qtree, UniformDivision)
assign_shapes(qtree)

dwg = svgwrite.Drawing('out/test.svg', profile='tiny')
draw_grids(dwg, qtree, PAGE_SIZE, False)
dwg.save()
