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
        if self.height > 0:
            heightValue = ((self.height / 1000.0)) * 255
            heightValue = min(max(heightValue, 0), 255)
            color = (heightValue*0.5, heightValue, heightValue*0.5)
        else:
            heightValue = (1+(self.height / 1000.0))*127
            heightValue = min(max(heightValue, 0), 255)
            color = (heightValue*0.1, heightValue*0.1, heightValue)
        surface.fill(color, rect)

