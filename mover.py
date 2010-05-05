import random

class Mover(object):
    """ A renderable object with a location, color, and movement method. """
    def __init__(self, grid, location, color):
        self.grid = grid
        self.node = grid.get_node_at(location)
        self.color = color
    
    def move(self):
        pass

    def get_location(self):
        return self.node.location

    def render(self, area, surface):
        surface.fill(self.color, area)


class RandomMover(Mover):
    """ A mover that moves randomly between adjacent nodes. """
    def __init__(self, grid, location, color=(255, 0, 0)):
        Mover.__init__(self, grid, location, color)

    def move(self):
        neighbors = self.grid.neighbors(self.node)
        self.node = random.choice(neighbors)
