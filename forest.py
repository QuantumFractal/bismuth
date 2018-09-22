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


def insert_point(root, pos, depth=0):

    if root is None:
        return kdNode(pos)

    cd_idx = depth % K
    if (pos[cd_idx] < root.point[cd_idx]):
        root.left = insert_point(root.left, pos, depth=depth+1)
    else:
        root.right = insert_point(root.right, pos, depth=depth+1)
    return root


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


points = [(3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7), (10, 19)]
print(points)
tree = None
for point in points:
    tree = insert_point(tree, point)


print_tree(tree)
