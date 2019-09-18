""" Library for lerps, and more fun things """

class Interpolate():
    def __init__(self, function):
        self.function = function

    def step(self, t):
        return self.function(t)