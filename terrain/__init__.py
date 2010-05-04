import random, pygame, math

class TerrainData():
    def __init__(self):
        self.height = 0 # in meters, arbitrarily
        self.moisture = 0 # 0..1 implies humid land, 1+ equals meters of water coverage
        self.temperature = 0 # 0..1

    def randomize(self):
        self.height = (random.random() - 0.5)*1000
        self.moisture = random.random()
        self.temperature = random.random()

    def render(self, rect, surface):
        heightValue = ((self.height / 1000.0)+0.5) * 255
        if heightValue > 255:
            heightValue = 255
        if heightValue < 0:
            heightValue = 0
        color = (heightValue, heightValue, heightValue)
        surface.fill(color, rect)

