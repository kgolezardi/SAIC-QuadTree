import math


class Shape:
    @classmethod
    def draw(cls, dwg, position):
        raise NotImplementedError("You should implement this method")


class NoShape(Shape):
    @classmethod
    def draw(cls, dwg, position):
        pass


class Circle(Shape):
    STROKE_WIDTH_PERCENTAGE = 0.20

    @classmethod
    def draw(cls, dwg, position):
        x1, y1, x2, y2 = position
        center = ((x1 + x2) / 2, (y1 + y2) / 2)
        cell_width = x2 - x1
        radius = cell_width * (1 - cls.STROKE_WIDTH_PERCENTAGE) / 2
        stroke_width = cell_width * cls.STROKE_WIDTH_PERCENTAGE
        dwg.add(dwg.circle(center=center, r=radius, fill='none', stroke='black', stroke_width=stroke_width))


class Rectangle(Shape):
    @classmethod
    def draw(cls, dwg, position):
        x1, y1, x2, y2 = position
        cell_width = x2 - x1
        dwg.add(dwg.rect(insert=(x1, y1), size=(cell_width, cell_width), fill='blue'))


class Polygon(Shape):
    COLOR = None

    @classmethod
    def raw_points(cls):
        raise NotImplementedError("You should implement this method")

    @classmethod
    def draw(cls, dwg, position):
        if cls.COLOR is None:
            raise NotImplementedError("Certain variables should be set in derived class")

        raw_points = cls.raw_points()
        points = []
        x1, y1, x2, y2 = position
        cell_width = x2 - x1
        center = ((x1 + x2) / 2, (y1 + y2) / 2)
        for x, y in raw_points:
            # x = x * cell_width * (1 - cls.STROKE_WIDTH_PERCENTAGE) / 2 + center[0]
            # y = y * cell_width * (1 - cls.STROKE_WIDTH_PERCENTAGE) / 2 + center[1]

            x = x * cell_width / 2 + center[0]
            y = y * cell_width / 2 + center[1]
            points.append((x, y))
        # stroke_width = cell_width * cls.STROKE_WIDTH_PERCENTAGE
        # dwg.add(dwg.polygon(points=points, fill='none', stroke=cls.COLOR, stroke_width=stroke_width))
        dwg.add(dwg.polygon(points=points, fill=cls.COLOR))


class RegularPolygon(Polygon):
    STROKE_WIDTH_PERCENTAGE = None
    SIDE_NUMBERS = None

    @classmethod
    def raw_points(cls):
        if cls.STROKE_WIDTH_PERCENTAGE is None or cls.SIDE_NUMBERS is None:
            raise NotImplementedError("Certain variables should be set in derived class")

        teta = 2 * math.pi / cls.SIDE_NUMBERS
        points = []
        for i in range(cls.SIDE_NUMBERS):
            x = math.cos(i * teta)
            y = math.sin(i * teta)
            points.append((x, y))
        return points


class Decagon(RegularPolygon):
    STROKE_WIDTH_PERCENTAGE = 0.5
    SIDE_NUMBERS = 10
    COLOR = 'red'


class Octagon(RegularPolygon):
    STROKE_WIDTH_PERCENTAGE = 0.5
    SIDE_NUMBERS = 8
    COLOR = 'green'


class BackSlash(Polygon):
    COLOR = 'brown'

    @classmethod
    def raw_points(cls):
        points = [(-1, -1), (-1, -0.5), (1, 1), (1, 0.5)]
        return points


class Slash(Polygon):
    COLOR = 'pink'

    @classmethod
    def raw_points(cls):
        points = [(1, -1), (1, -0.5), (-1, 1), (-1, 0.5)]
        return points
