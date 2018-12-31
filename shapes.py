class Shape:
    @classmethod
    def draw(cls, dwg, position):
        raise NotImplementedError("You should implement this method")


class NoShape(Shape):
    @classmethod
    def draw(cls, dwg, position):
        pass


class Circle(Shape):
    STROKE_WIDTH_PERCENTAGE = 0.25
    @classmethod
    def draw(cls, dwg, position):
        x1, y1, x2, y2 = position
        center = ((x1 + x2) / 2, (y1 + y2) / 2)
        cell_width = x2 - x1
        radius = cell_width * (1 - cls.STROKE_WIDTH_PERCENTAGE) / 2
        stroke_width = cell_width * cls.STROKE_WIDTH_PERCENTAGE
        dwg.add(dwg.circle(center=center, r=radius, fill='white', stroke='black', stroke_width=stroke_width))


class Rectangle(Shape):
    @classmethod
    def draw(cls, dwg, position):
        x1, y1, x2, y2 = position
        cell_width = x2 - x1
        dwg.add(dwg.rect(insert=(x1, y1), size=(cell_width, cell_width), fill='blue'))
