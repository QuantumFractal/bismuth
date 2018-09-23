import math
import colorsys
import random

K = 2

class kdNode:
    def __init__(self, point, data={}):
        self.left, self.right = None, None
        assert len(point) == K
        self.point = point
        self.data = data

    def __str__(self):
        return (f"""<{','.join(str(dim) for dim in self.point)}> """+
               f"""L: {'none' if self.left is None else ','.join(str(dim) for dim in self.left.point)}, """+
               f"""R: {'none' if self.right is None else ','.join(str(dim) for dim in self.right.point)}""")

    def is_leaf(self):
        return self.left is None and self.right is None



class boundingBox:
    def __init__(self, x1, y1, x2, y2):
        self.min = (min(x1, x2), min(y1, y2))
        self.max = (max(x1, x2), max(y1, y2))

    def __str__(self):
        return f"[({self.min[0]}, {self.min[1]}), ({self.max[0]}, {self.max[1]})]"


    def __contains__(self, point):
        assert len(point) == 2
        return self.min[0] <= point[0] <= self.max[0] and self.min[1] <= point[1] <= self.max[1]


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

    def draw(self, ctx):
        ctx.save()
        hue = random.uniform(0, 1)
        ctx.set_source_rgba(*colorsys.hsv_to_rgb(hue, .75, .75), .75)
        ctx.set_line_width(4)
        ctx.set_dash([5])
        ctx.rectangle(self.min[0], self.min[1], self.max[0] - self.min[0], self.max[1] - self.min[1])
        ctx.stroke()
        ctx.arc(*self.min, 3, 0, 7)
        ctx.move_to(*self.max)
        ctx.arc(*self.max, 3, 0, 7)
        ctx.fill()
        ctx.restore()


def nearestNeighbor(point, node, ref_point, ref_distance=math.inf, depth=0):

    if node is None:
        return

    if node.is_leaf():
        new_dist = dist(point, node.point)
        if new_dist < ref_distance:
            ref_distance = new_dist
            ref_point = node.point
    else:
        dim = depth % K
        if point[dim] <= node.point[dim]:
            if point[dim] - ref_distance <= node.point[dim]:
                return nearestNeighbor(point, node.left, ref_point, ref_distance, depth=depth+1)
            if point[dim] + ref_distance > node.point[dim]:
                return nearestNeighbor(point, node.right, ref_point, ref_distance, depth=depth+1)
        else:
            if point[dim] + ref_distance > node.point[dim]:
                return nearestNeighbor(point, node.right, ref_point, ref_distance, depth=depth+1)
            if point[dim] - ref_distance <= node.point[dim]:
                return nearestNeighbor(point, node.left, ref_point, ref_distance, depth=depth+1)


def dist(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def insert_point(root, pos, depth=0):

    if root is None:
        return kdNode(pos)

    cd_idx = depth % K
    if (pos[cd_idx] < root.point[cd_idx]):
        root.left = insert_point(root.left, pos, depth=depth+1)
    else:
        root.right = insert_point(root.right, pos, depth=depth+1)
    return root


def draw_tree(ctx, root, bb, depth=0):

    if root is None:
        return

    bb.draw(ctx)
    ctx.save()
    ctx.set_source_rgb(1,1,1)
    ctx.arc(*root.point, 3, 0, 7)
    ctx.fill()
    ctx.restore()
    dim = depth % K

    if dim == 0:
        left_b, right_b = bb.divide_vertical(root.point[0])
    else:
        left_b, right_b = bb.divide_horizonal(root.point[1])

    draw_tree(ctx, root.left, left_b, depth=depth+1)
    draw_tree(ctx, root.right, right_b, depth=depth+1)


"""
cd_idx = depth % K
if cd_idx == 0: # X line
    ctx.set_source_rgba(1, 0, 0, .5)
    ctx.move_to(bounds[0], root.point[1])
    ctx.line_to(bounds[1], root.point[1])
    ctx.stroke()
    left_bounds = (bounds[0], root.point[1])
    right_bounds = (root.point[1], bounds[1])
else: # Y line
    ctx.set_source_rgba(0, 1, 0, .5)
    ctx.move_to(root.point[0], bounds[0])
    ctx.line_to(root.point[0], bounds[1])
    ctx.stroke()
    left_bounds = (bounds[0], root.point[0])
    right_bounds = (root.point[0], bounds[1])

ctx.set_source_rgb(1,1,1)
ctx.arc(*root.point, 4, 0, math.pi*2)
ctx.fill()

print(f"LEFT BOUNDS: {left_bounds}, RIGHT BOUNDS: {right_bounds}")
draw_tree(ctx, root.left, left_bounds, width, height, depth=depth+1)
draw_tree(ctx, root.right, right_bounds, width, height, depth=depth+1)
"""

def print_tree(root, indent='', last=False):
    if root is None:
        return
    
    print(indent, end='')
    if last:
        print('└-', end='')
        indent += "  "
    else: 
        print('├-', end='')
        indent += "| "
    print(root.point)


    print_tree(root.left, indent=indent, last=False)
    print_tree(root.right, indent=indent, last=True)


"""
points = [(3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7), (10, 19)]
print(points)
tree = None
for point in points:
    tree = insert_point(tree, point)


print_tree(tree)
"""