""" Root based life form """
import util
import math
import random
from collections import deque
import forest


class Roots:

    def __init__(self, seed, bounds):
        self.seed = seed          

        # Hack for now
        self.bounds = bounds
        self.kd = forest.kdTree(self.bounds)

        # Leaves all points without children
        self.leaves= set([self.seed])
        self.nonleaves = set()
        self.max_cells = 100
    
    def reset(self):
        self.seed.children = []
        self.leaves = set([self.seed])
        self.nonleaves = set()
        self.kd = forest.kdTree(self.bounds)
        self.max_cells = 100

    def can_grow(self):
        return len(self.leaves) + len(self.nonleaves) < self.max_cells

    def grow_once(self, position=None):

        tries = 10
        envelope = 0
        wiggle = math.radians(60)
        

        # Probablity of a split or a new leaf
        if random.random() <= 1:
            leaf = random.sample(self.leaves, 1)[0]
            new_size = 15

            # We're making a new leaf
            # Keep trying, wigglings, reducing size
            while tries > 0:
                new_size = max(new_size - 1, 5)
                wiggle += math.radians(5)
                new_direction = random.uniform(leaf.direction - wiggle, leaf.direction + wiggle)

                new_position = self.calculate_offset(new_direction, new_size, leaf)

                self.kd.delete(leaf.position)
                nearest = self.kd.nearestNeighbor(new_position)
                self.kd.insert(leaf.position, data={'size':leaf.size})
                
                neighbor_collision = nearest is None or forest.distance(nearest.point, new_position) > (nearest.data['size'] + new_size + envelope)
                box_collision = new_position in self.bounds

                if neighbor_collision and box_collision:
                    # Create and link our new cell
                    new_leaf = Cell(position=new_position, direction=new_direction, size=new_size, parent=leaf)
                    leaf.children.append(new_leaf)

                    # Book keeping for new leaf
                    self.leaves.add(new_leaf)
                    self.kd.insert(new_position, data={'size':new_size})

                    # Book keeping for old leaf
                    self.leaves.remove(leaf)
                    self.nonleaves.add(leaf)

                    break
                else:
                    tries -= 1

        # Otherwise we split   
        else:
            nonleaf = random.sample(self.nonleaves, 1)[0]
            new_size = 10
            new_direction = random.uniform(nonleaf.direction - wiggle, nonleaf.direction + wiggle)


    def calculate_offset(self, direction, size, leaf):
        new_position = ((leaf.size + size) * math.cos(direction) + leaf.position[0],
                        (leaf.size + size) * math.sin(direction) + leaf.position[1])
        return new_position



    def draw(self, ctx):
        stack = list([self.seed])
        while len(stack) > 0:
            cur = stack.pop()

            for child in cur.children:
                util.draw_segment_outfill(ctx, cur.position, child.position, cur.size, child.size, (1, 1, 1))
                stack.append(child)
            parent = cur.parent or cur
            util.draw_segment_infill(ctx, parent.position, cur.position, parent.size, cur.size, (1, 1, 1))
        self.bounds.draw(ctx)

class Cell:
    def __init__(self, position=(0,0), direction=0, size=20, parent=None):
        self.parent = parent
        self.position = position
        self.size = size
        self.children = []
        self.direction = direction

    def __str__(self):
        return f"Cell <{self.position[0]:1.2f},{self.position[1]:1.2f}>"