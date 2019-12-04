from random import randint

rect = {'tag': 'rect', 'x': 10.0, 'y': 10.0, 'width': 30.0, 'height': 30.0}


def generate_random_rects(amount):
    rects = []
    for c in range(amount):
        x, y = randint(0,100), randint(0, 100)
        w, h = randint(0,40), randint(0, 40)
        r = {'tag': 'rect', 'x': x, 'y': y, 'width': w, 'height':h}
        rects.append(r)
    return rects

def generate_points(r):
    return [Pair(r['x'], r['y']), 
            Pair(r['x'] + r['width'], r['y']), 
            Pair(r['x'] + r['width'], r['y'] + r['height']),
            Pair(r['x'], r['y'] + r['height'])]


def dist2(p1, p2):
    return (p2.y - p1.y) ** 2 + (p2.x - p1.x) ** 2


class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Pair({}, {})".format(self.x, self.y)

    def __hash__(self):
        """ Hash this like a tuple """
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def dist2(self, p):
        return (p.x - self.x) ** 2 + (p.y - self.y) ** 2

    

class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def __str__(self):
        return "Edge(({}, {}) <-> ({}, {}))".format(self.p1.x, self.p1.y, self.p2.x, self.p2.y)

    def __hash__(self):
        """ Slightly clever hash, always picking the lowest value.
            Now all look ups for [1,2] -> [2,1] will match [2,1] -> [1,2]
        """
        return min(hash((self.p1, self.p2)), 
                   hash((self.p2, self.p1)))

    def __eq__(self, other):
        return self.p1 == other.p2 and self.p2 == other.p2

    def dist2(self):
        return self.p2.dist2(p1)

p1 = Pair(1,2)
p2 = Pair(10,10)

e1 = Edge(p1, p2)
e2 = Edge(p1, p2)


print(e1)

# Represents the distance between points, we'll use the distance^2 for speed.
# Graph is fully connected, so worst case TSP :(
GRAPH = {}
POINTS = []

components = generate_random_rects(2)

for component in components:
    points = generate_points(component)
    p1 = points[0]
    # calculate distance between new points any everyone else
    for point in points:
        print(point.dist2(p1))
