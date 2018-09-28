""" Utilities module """
import random


class boundingBox:
    def __init__(self, x1, y1, x2, y2):
        self.min = (min(x1, x2), min(y1, y2))
        self.max = (max(x1, x2), max(y1, y2))

    def __str__(self):
        return f"[({self.min[0]}, {self.min[1]}), ({self.max[0]}, {self.max[1]})]"


    def __contains__(self, point):
        assert len(point) == 2
        return self.min[0] <= point[0] <= self.max[0] and self.min[1] <= point[1] <= self.max[1]

    def get_center(self):
        x = (self.max[0] - self.min[0]) / 2
        y = (self.max[1] - self.min[0]) / 2
        return (x, y)

    def divide_vertical(self, x):
        assert self.min[0] <= x <= self.max[0]
        left = boundingBox(*self.min, x, self.max[1])
        right = boundingBox(x, self.min[1], *self.max)
        return left, right
    
    def divide_horizonal(self, y):
        assert self.min[1] <= y <= self.max[1]
        left = boundingBox(*self.min, self.max[0], y)
        right = boundingBox(self.min[0], y, *self.max)
        return left, right

    def distance(self, point):
        d_x = max(self.min[0] - point[0], point[0] - self.max[0])
        d_y = max(self.min[1] - point[1], point[1] - self.max[1])
        return math.sqrt(d_x**2 + d_y**2)
        
    def get_random_point(self):
        x = random.randint(self.min[0], self.max[0])
        y = random.randint(self.min[1], self.max[1])
        return (x, y)

    def draw(self, ctx):
        ctx.save()
        hue = random.uniform(0, 1)
        ctx.set_source_rgba(*colorsys.hsv_to_rgb(hue, .75, .75), .25)
        ctx.set_line_width(4)
        ctx.set_dash([5])
        ctx.rectangle(self.min[0], self.min[1], self.max[0] - self.min[0], self.max[1] - self.min[1])
        ctx.stroke()
        ctx.arc(*self.min, 3, 0, 7)
        ctx.move_to(*self.max)
        ctx.arc(*self.max, 3, 0, 7)
        ctx.fill()
        ctx.restore()

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)