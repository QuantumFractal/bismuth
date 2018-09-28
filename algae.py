""" Algae life form """
import forest
import util

import colorsys
import math


class Cluster:
    def __init__(self, seed, bounds):
        self.seed = seed
        self.bounds = bounds
        self.cells = {}
        self.cells[self.seed.position] = self.seed
        self.envelope = 70
        self.population_cap = 500
        self.kd_tree = forest.kdNode(seed.position)
        self.last_guess = (0,0)

    def reset(self):
        self.cells = set()
        self.cells.add(self.seed)
        self.kd_tree = forest.kdNode(self.seed.position)
        self.last_guess = (0,0)

    def grow_cell(self):
        if len(self.cells) > 100:
            return

        # Get a random point
        position = self.bounds.get_random_point()
        self.last_guess = position

        # Search for the nearest cell
        nearestNeighbor = forest.bestNN(position, self.kd_tree)
        distance = forest.distance(nearestNeighbor.point, position)

        center = self.bounds.get_center()
        dx = position[0] - center[0]
        dy = position[1] - center[1]

        angle = math.degrees(math.atan2(dy, dx))
        hue = util.translate(angle, -180, 180, 0, 1)
        value = 1 - util.translate(forest.distance(center, position), 0, 500, 0, 1)
        color = colorsys.hsv_to_rgb(hue, .9, value)
        
        # Lookup cell
        cell = self.cells[nearestNeighbor.point]

        # If the new point happens to be in range of our closest neighbor
        if cell.size <= distance <= self.envelope:
            new_cell = Cell(position=position, color=color)
            self.kd_tree = forest.insert_point(self.kd_tree, position)
            self.cells[position] = new_cell

        
    def draw(self, ctx):
        for cell in self.cells.values():
            cell.draw(ctx)
        ctx.save()
        ctx.set_source_rgb(.7,0,0)
        ctx.arc(*self.last_guess, 5, 0, 7)
        ctx.fill()
        ctx.restore()
   
class Cell:
    def __init__(self, position=(0,0), size=20, color=(0.2, 1, 0.2)):
        self.position = position
        self.size = size
        self.color = color
    
    def draw(self, ctx):
        ctx.save()
        hsv = colorsys.rgb_to_hsv(*self.color)
        darker = colorsys.hsv_to_rgb(hsv[0], hsv[1] + 0.1, hsv[2])
        ctx.set_source_rgba(*darker, 1)
        ctx.arc(*self.position, self.size, 0, 7)
        ctx.stroke()
        ctx.arc(*self.position, self.size, 0, 7)
        ctx.set_source_rgba(*self.color, 0.5)
        ctx.fill()