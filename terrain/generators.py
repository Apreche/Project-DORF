import random, math 

class TerrainGenerator:
	def apply(self, grid):
		pass

class MeteorTerrainGenerator(TerrainGenerator):
    def __init__(self, strikes=25, strikeMinRadius=20, strikeMaxRadius=100):
        self.strikes = strikes
        self.strikeMinRadius = strikeMinRadius
        self.strikeMaxRadius = strikeMaxRadius

    def apply(self, grid):
        for i in range(0, self.strikes):
            minX, minY, minZ = grid.min
            maxX, maxY, maxZ = grid.max
            randX = random.randint(minX, maxX)
            randY = random.randint(minY, maxY)
            strikeLocation = (randX, randY, 0)
            strikeNode = grid.get_node_at(strikeLocation)

            strikeRadius = random.randint(self.strikeMinRadius, self.strikeMaxRadius)
            sqrStrikeRadius = strikeRadius * strikeRadius

            if strikeNode is None:
                print "Out-of-range meteor strike at ", 
                print strikeLocation

            for node in grid.nodes():
                nodeX, nodeY, nodeZ = node.location
                strikeX, strikeY, strikeZ = strikeLocation
                x_pow = math.pow(nodeX - strikeX, 2)
                y_pow = math.pow(nodeY - strikeY, 2)
                sqrDistance = x_pow + y_pow

                """
                meteor profile is essentially a cosine curve 
                (high at the center, falls off, high again at 
                the crater edge)
                this is not exactly right, but close enough for 
                the moment
                cubing creates a bit more of a reasonable "crater"
                """
                terrainData = node.contents
                if sqrDistance < sqrStrikeRadius:
                    change = math.pow(math.cos(sqrDistance / sqrStrikeRadius * math.pi * 3), 3)
                    change *= (1 - (sqrDistance / sqrStrikeRadius))
                    change *= strikeRadius * 3
                    terrainData.height += change
