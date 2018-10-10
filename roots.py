""" Root based life form """
import util
import math
import random
from collections import deque
import forest


class Roots:

    def __init__(self, seed, bounds, kd=None):
        self.seed = seed          

        # Hack for now
        if kd is None:
            self.bounds = bounds
            self.kd = forest.kdTree(self.bounds)
        else:
            self.bounds = kd.bounds
            self.kd = kd

        # Leaves all points without children
        self.leaves= set([self.seed])
        self.nonleaves = set()
        self.max_cells = 1000
    
    def reset(self):
        self.seed.children = []
        self.leaves = set([self.seed])
        self.nonleaves = set()
        #self.kd = forest.kdTree(self.bounds)
        self.kd.clear()
        self.max_cells = 1000

    def can_grow(self):
        return len(self.leaves) + len(self.nonleaves) < self.max_cells

    def grow_once(self, position=None, ctx=None):

        tries = 10
        envelope = 0

        
        split_chance = (2*(len(self.leaves) + 1)) /(len(self.nonleaves) + 1) 

        # Probablity of a split or a new leaf
        if random.random() <= 0.3:
            if len(self.leaves) == 0:
                return 
    
            leaf = random.sample(self.leaves, 1)[0]
            new_size = leaf.size

            # Dead leaf!
            if new_size < 10:
                self.leaves.remove(leaf)
                return
            
            wiggle = math.radians(50)
            # We're making a new leaf
            # Keep trying, wigglings, reducing size
            while tries > 0:
                new_size = max(new_size - 1, 5)
                wiggle += math.radians(5)
                new_direction = random.uniform(leaf.direction - wiggle, leaf.direction + wiggle)

                new_position = self.calculate_offset(new_direction, new_size, leaf)

                if ctx is not None:
                    util.draw_point(ctx, *new_position)

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
            # If we've exhausted this leaf, let's not try it again!
            if tries < 0:
                self.leaves.remove(leaf)

        # Otherwise we split   
        else:
            if len(self.nonleaves) == 0:
                return
            nonleaf = random.sample(self.nonleaves, 1)[0]
            parent = nonleaf.parent
            tries = 10

            if parent is None:
                p_angle = 0
            else:
                p_angle = parent.direction
            
            # Wiggle is how far we're willing to deviate from our parent's direction
            # Reach is how far we're willing to stretch to make a new branch
            wiggle = math.radians(10)
            reach = 0
            new_size = nonleaf.size

            while tries > 0:
                tries -= 1

                wiggle += math.radians(10)
                reach += .2
                new_size = max(new_size - .2, 5)
                
                # Check which side to split on
                if nonleaf.direction - p_angle < 0:
                    new_direction = p_angle - math.radians(40)
                else: 
                    new_direction = p_angle + math.radians(40)

                # Wiggle it a bit!
                new_direction = random.uniform(new_direction - wiggle, new_direction + wiggle)
                new_direction = p_angle - math.radians(40) if nonleaf.direction - p_angle < 0 else p_angle+ math.radians(40)

                # Dead leaf!
                if new_size < 3:
                    self.nonleaves.remove(nonleaf)
                    return

                new_position = self.calculate_offset(new_direction, new_size, nonleaf, reach=reach)
                if ctx is not None:
                    util.draw_point(ctx, *new_position)


                self.kd.delete(nonleaf.position)
                if parent is not None:
                    self.kd.delete(parent.position)

                nearest = self.kd.nearestNeighbor(new_position)

                self.kd.insert(nonleaf.position, data={'size': nonleaf.size})
                if parent is not None:
                    self.kd.insert(parent.position, data={'size': nonleaf.size})
                
                neighbor_collision = nearest is None or forest.distance(nearest.point, new_position) > (nearest.data['size'] + new_size + envelope)
                box_collision = new_position in self.bounds

                if neighbor_collision and box_collision:
                    new_leaf = Cell(position=new_position, direction=new_direction, size=new_size, parent=nonleaf)
                    nonleaf.children.append(new_leaf)

                    self.leaves.add(new_leaf)
                    self.kd.insert(new_leaf.position, data={'size':new_leaf.size})  
                    break
            # If we've exhausted this branch position, let's not try it again
            if tries < 0:
                self.nonleaves.remove(nonleaf)

    def calculate_offset(self, direction, size, leaf, reach=0):
        new_position = ((leaf.size + size + reach) * math.cos(direction) + leaf.position[0],
                        (leaf.size + size + reach) * math.sin(direction) + leaf.position[1])
        return new_position



    def draw(self, ctx):
        envelope = 10
        min_size = 5
        stack = list([self.seed])
        while len(stack) > 0:
            cur = stack.pop()

            for child in cur.children:
                util.draw_segment_outfill(ctx, cur.position, child.position, max(cur.size - envelope, min_size), max(child.size - envelope, min_size), (65/256, 175/256, 98/256))
                stack.append(child)
            parent = cur.parent or cur
            util.draw_segment_infill(ctx, parent.position, cur.position, max(parent.size - envelope, min_size), max(cur.size - envelope, min_size), (65/256, 175/256, 98/256))
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