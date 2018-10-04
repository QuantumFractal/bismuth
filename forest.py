import math
import colorsys
import random
from util import boundingBox

K = 2

class kdNode:
    def __init__(self, point, parent=None, data={}):
        self.left, self.right = None, None
        self.parent = parent
        assert len(point) == K
        self.point = point
        self.data = data

    def __str__(self):
        return (f"""<{','.join(str(dim) for dim in self.point)}> """)

               #f"""L: {'none' if self.left is None else ','.join(str(dim) for dim in self.left.point)}, """+
               #f"""R: {'none' if self.right is None else ','.join(str(dim) for dim in self.right.point)}""")

    def is_leaf(self):
        return self.left is None and self.right is None


class kdTree:
    def __init__(self, bounds, K=2):
        self.root = None
        self.bounds = bounds
        self.K = K

    def insert(self, point, data=None):        
        if self.root is None:
            self.root = kdNode(point, data=data)
        else:
            self._insert(self.root, point, self.root, data, depth=0)

    def delete(self, point):
        self.root = self._delete(self.root, point, depth=0)

    def findMin(self):
        if self.root is None:
            return None
        return self._findMin(self.root, 0, depth=0)

    def draw(self, ctx):
        if self.root is None:
            return 

        self._draw(ctx, self.root, self.bounds, depth=0)

    def nearestNeighbor(self, point):
        return self._NN(point, self.root)
    

    def _insert(self, root, point, parent, data, depth):
        if root is None:
            return kdNode(point, parent=parent, data=data)

        cd_idx = depth % K
        if point == root.point:
            return root
        
        if (point[cd_idx] < root.point[cd_idx]):
            root.left = self._insert(root.left, point, root, data=data, depth=depth+1)
        else:
            root.right = self._insert(root.right, point, root, data=data, depth=depth+1)
        return root


    def _delete(self, node, point, depth=0):
        dim = depth % self.K

        indent = "-"*depth
        # Dead end!
        if node is None:
            return None
            
        # We found a match
        if node.point == point:
            # If we're a leaf, just remove ourselves
            # Root special case

            # Otherwise copy data from the minimum node (left or right)
            # and delete it recursively.
            if node.right is not None:
                print(indent+" Seaching right for min...")
                r_min = self._findMin(node.right, dim, depth=depth+1)
                print(indent+f" Found {r_min}")
                node.point = r_min.point
                node.data = r_min.data
                node.right = self._delete(node.right, r_min.point, depth=depth+1)

            elif node.left is not None:
                l_min = self._findMin(node.left, dim, depth=depth+1)
                node.point = l_min.point
                node.data = l_min.data
                node.right = self._delete(node.left, l_min.point, depth=depth+1)
                node.left = None
            else:
                node = None
            return node

        # Keep looking
        elif point[dim] < node.point[dim]:
            node.left = self._delete(node.left, point, depth=depth+1)
        else:
            node.right = self._delete(node.right, point, depth=depth+1)
        return node

    def _findMin(self, node, dim, depth=0):
        if node is None:
            return None

        if dim == depth % self.K:
            if node.left is None:
                return node
            return self._findMin(node.left, dim, depth=depth+1)
        
        l_min = self._findMin(node.left, dim, depth=depth+1)
        r_min = self._findMin(node.right, dim, depth=depth+1)
        return min([node, l_min, r_min], key=lambda n: math.inf if n is None else n.point[dim])


    def _draw(self, ctx, root, bb, depth=0):
        bb.draw(ctx)
        if root is None:
            return

        dim = depth % K

        if dim == 0:
            left_b, right_b = bb.divide_vertical(root.point[0])
        else:
            left_b, right_b = bb.divide_horizonal(root.point[1])

        self._draw(ctx, root.left, left_b, depth=depth+1)
        self._draw(ctx, root.right, right_b, depth=depth+1)
        ctx.save()
        ctx.set_source_rgb(0, 0, 0)
        ctx.arc(*root.point, 3, 0, 7)
        ctx.fill()
        ctx.restore()


    def _NN(self, query, tree, best_node=None, best_dist=math.inf, depth=0):
        # We've exhausted the search
        # as a leaf node or as a child
        if tree is None or tree.is_leaf():
            return tree

        # Check if this node is closer than our best.
        this_dist = distance(query, tree.point)
        if this_dist < best_dist:
            best_node = tree
            best_dist = this_dist

        dim = depth % K
        next_depth = depth + 1

        # Search the left subtree first
        if query[dim] < tree.point[dim] and tree.left is not None:
            left_best = self._NN(query, tree.left, best_node=best_node, best_dist=best_dist, depth=next_depth)
            left_dist = distance(query, left_best.point)

            # Update our best guesses
            if left_dist < best_dist:
                best_node = left_best
                best_dist = left_dist

            # Check if the solution might be in a different subtree
            if query[dim] + distance(query, best_node.point) > tree.point[dim] and tree.right is not None:
                right_best = self._NN(query, tree.right, best_node=best_node, best_dist=best_dist, depth=next_depth)
                right_dist = distance(query, right_best.point)

                # Update our best guesses again
                if right_dist < best_dist:
                    best_node = right_best

        # Search the right subtree
        elif tree.right is not None:
            right_best = self._NN(query, tree.right, depth=next_depth)
            right_dist = distance(query, right_best.point)
            if right_dist < best_dist:
                best_node = right_best
                best_dist = right_dist
        
            if query[dim] - distance(query, best_node.point) < tree.point[dim] and tree.left is not None:
                left_best = self._NN(query, tree.left, best_node=best_node, best_dist=best_dist, depth=next_depth)
                left_dist = distance(query, left_best.point)
                if left_dist < best_dist:
                    best_node = left_best
        
        return best_node

def bestNN(query, tree, best_node=None, best_dist=math.inf, depth=0):

    # We've exhausted the search
    # as a leaf node or as a child
    if tree is None or tree.is_leaf():
        return tree

    # Check if this node is closer than our best.
    this_dist = distance(query, tree.point)
    if this_dist < best_dist:
        best_node = tree
        best_dist = this_dist

    dim = depth % K
    next_depth = depth + 1

    # Search the left subtree first
    if query[dim] < tree.point[dim] and tree.left is not None:
        left_best = bestNN(query, tree.left, best_node=best_node, best_dist=best_dist, depth=next_depth)
        left_dist = distance(query, left_best.point)

        # Update our best guesses
        if left_dist < best_dist:
            best_node = left_best
            best_dist = left_dist

        # Check if the solution might be in a different subtree
        if query[dim] + distance(query, best_node.point) > tree.point[dim] and tree.right is not None:
            right_best = bestNN(query, tree.right, best_node=best_node, best_dist=best_dist, depth=next_depth)
            right_dist = distance(query, right_best.point)

            # Update our best guesses again
            if right_dist < best_dist:
                best_node = right_best

    # Search the right subtree
    elif tree.right is not None:
        right_best = bestNN(query, tree.right, depth=next_depth)
        right_dist = distance(query, right_best.point)
        if right_dist < best_dist:
            best_node = right_best
            best_dist = right_dist
    
        if query[dim] - distance(query, best_node.point) < tree.point[dim] and tree.left is not None:
            left_best = bestNN(query, tree.left, best_node=best_node, best_dist=best_dist, depth=next_depth)
            left_dist = distance(query, left_best.point)
            if left_dist < best_dist:
                best_node = left_best
    
    return best_node
    

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def insert_point(root, pos, data={}, depth=0):

    if root is None:
        return kdNode(pos, data=data)

    cd_idx = depth % K
    if (pos[cd_idx] < root.point[cd_idx]):
        root.left = insert_point(root.left, pos, data=data, depth=depth+1)
    else:
        root.right = insert_point(root.right, pos, data=data, depth=depth+1)
    return root



def draw_tree(ctx, root, bb, depth=0):

    #bb.draw(ctx)
    if root is None:
        return

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

def print_tree(root, indent='', prefix='', last=False):
    if root is None:
        return
    
    print(indent, end='')
    if last:
        print('└-'+prefix, end='')
        indent += "  "
    else: 
        print('├-'+prefix, end='')
        indent += "  "
    print(root.point)


    print_tree(root.left, indent=indent, prefix='L', last=False)
    print_tree(root.right, indent=indent, prefix='R', last=True)



"""
points = [(3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7), (10, 19)]
print(points)
tree = None
for point in points:
    tree = insert_point(tree, point)


print_tree(tree)
"""