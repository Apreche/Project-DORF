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


class TerrainGenerator():
	def apply(self, grid):
		pass

class MeteorTerrainGenerator(TerrainGenerator):
	def __init__(self, strikes=25, strikeMinRadius=20, strikeMaxRadius=100):
		self.strikes = strikes
		self.strikeMinRadius = strikeMinRadius
		self.strikeMaxRadius = strikeMaxRadius
	
	def apply(self, grid):
		for i in range(0, self.strikes):
			strikeLocation = (random.randint(grid.minX, grid.maxX), random.randint(grid.minY, grid.maxY), -1)
			strikeNode = grid.get_node_at(strikeLocation)

			strikeRadius = random.randint(self.strikeMinRadius, self.strikeMaxRadius)
			sqrStrikeRadius = strikeRadius * strikeRadius

			if None == strikeNode:
				print "Out-of-range meteor strike at ", 
				print strikeLocation


			for node in grid.nodes():
				if node.location[2] == -1:
					terrainData = node.contents
					sqrDistance = math.pow(node.location[0] - strikeLocation[0], 2) + math.pow(node.location[1] - strikeLocation[1], 2)

					# meteor profile is essentially a cosine curve 
					# (high at the center, falls off, high again at 
					# the crater edge)
					# this is not exactly right, but close enough for 
					# the moment
					# cubing creates a bit more of a reasonable "crater"
					if sqrDistance < sqrStrikeRadius:
						change = math.pow(math.cos(sqrDistance / sqrStrikeRadius * math.pi * 3), 3)
						change *= (1 - (sqrDistance / sqrStrikeRadius))
						change *= strikeRadius * 3
						terrainData.height += change


