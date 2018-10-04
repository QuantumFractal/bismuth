""" Root based life form """
import util
import math
import random
from collections import deque
import forest


class Roots:
    def __init__(self, seed):
        self.seed = seed
        self.queue_size = 2
        self.collision_queue = deque([None, None, None, None, self.seed], self.queue_size)
        self.last_added = None
        print(self.collision_queue)
        
            
        self.kd = None

        # Leaves all points without children
        self.leaves= set([seed])
        self.nonleaves = set()
    
    def reset(self):
        self.seed.children = []
        self.leaves = set([seed])
        self.nonleaves = set()
        self.kd = None

    def grow_once(self, position=None):

        tries = 10
        envelope = 0
        wiggle = math.radians(30)

        # Pop a cell out of the fifo
        if self.last_added is not None:
           pass

        # Probablity of a split or a new leaf
        if random.random() <= 1:
            leaf = random.sample(self.leaves, 1)[0]
            new_size = 10
            new_direction = random.uniform(leaf.direction - wiggle, leaf.direction + wiggle)

            # We're making a new leaf
            while tries > 0:
                new_position = self.calculate_offset(new_direction, new_size, leaf)

                nearest = forest.bestNN(new_position, self.kd)
                if nearest is None or forest.distance(nearest.point, new_position) > (nearest.data.size + new_size + envelope):
                    
                    new_leaf = Cell(position=new_position, direction=new_direction, size=new_size, parent=leaf)
                    leaf.children.append(new_leaf)

                    #self.kd = forest.insert_point(self.kd, new_position, data=new_leaf)
                    self.kd = forest.insert_point(self.kd, self.last_added.position, data=self.last_added)
                    self.leaves.remove(leaf)
                    self.leaves.add(new_leaf)
                    self.nonleaves.add(leaf)

                    # Check if this position works (kdTree)
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
                util.draw_segment_outfill(ctx, cur.position, child.position, cur.size, child.size, (.5, 1, .5))
                stack.append(child)
        

class Cell:
    def __init__(self, position=(0,0), direction=0, size=20, parent=None):
        self.parent = parent
        self.position = position
        self.size = size
        self.children = []
        self.direction = direction

    def __str__(self):
        return f"Cell <{self.position[0]:1.2f},{self.position[1]:1.2f}>"