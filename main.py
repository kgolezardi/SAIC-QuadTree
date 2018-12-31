import svgwrite

from divisions import UniformDivision

PAGE_SIZE = (0, 0, 700, 700)


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


def generate(quadtree, algorithm):
    algorithm.divide(quadtree)


qtree = QuadTree()
generate(qtree, UniformDivision)

dwg = svgwrite.Drawing('out/test.svg', profile='tiny')
draw_grids(dwg, qtree, PAGE_SIZE)
dwg.save()
