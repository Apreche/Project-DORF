import random, math, time

class TerrainGenerator:
    def apply(self, grid):
        pass

class MeteorTerrainGenerator(TerrainGenerator):
    """
    Modifies the heightmap by simulating some random "meteor strikes"

    Author: Alex Jarocha-Ernst
    """
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

class Smoother(TerrainGenerator):
    """
    Applies a simple smoothing filter to the height value of the grid
    Mostly just an example of a TerrainGenerator that's meant to be run
    in combination with others.

    Author: Alex Jarocha-Ernst
    """
    def __init__(self, smoothness=0.25):
        self.smoothness = smoothness

    def apply(self, grid):
        for node in grid.nodes():
            nodeX, nodeY, nodeZ = node.location
            neighbors = []
            neighbors.append(grid.get_node_at((nodeX+1, nodeY, nodeZ)))
            neighbors.append(grid.get_node_at((nodeX-1, nodeY, nodeZ)))
            neighbors.append(grid.get_node_at((nodeX, nodeY+1, nodeZ)))
            neighbors.append(grid.get_node_at((nodeX, nodeY-1, nodeZ)))
            neighbors.append(grid.get_node_at((nodeX, nodeY, nodeZ+1)))
            neighbors.append(grid.get_node_at((nodeX, nodeY, nodeZ-1)))

            original = node.contents.height
            avg = original
            total = 1
            for neighbor in neighbors:
                if neighbor is not None:
                    avg += neighbor.contents.height
                    total += 1

            avg /= total

            node.contents.height = avg*self.smoothness + node.contents.height*(1-self.smoothness)

class PlasmaFractalGenerator:
    """
    Generates a heightmap via a plasma fractal 
    (aka 2D midpoint displacement, aka diamond-squares algorithm)

    I suppose this could be expanded to generate values in three dimensions,
    which might be useful for some non-height pseudorandom data

    Author: Alex Jarocha-Ernst

    """
    def __init__(self, scale=100, seed=0):
        self.scale = scale
        self.seed = seed

    def randomizeSeed():
        self.seed = time.time()

    def apply(self, grid):
        random.seed(self.seed)

        minx, miny, minz = grid.min
        maxx, maxy, maxz = grid.max

        pairs = []

        pairs.extend(self._displacementPass(grid, (minx, miny, 0), (maxx, maxy, 0)))
        while len(pairs) > 0:
            """
            Each displacement pass adds four new (smaller) squares to process.
            Processing them in order is important; if all squares of size X 
            are not processed before squares of size X/2, pecular edge artifacts
            result.

            I tried doing this recursively first, but python's stack isn't
            large enough (and this is probably more efficient, anyway)

            """
            pair = pairs.pop(0)
            pairs.extend(self._displacementPass(grid, pair[0], pair[1]))

    def _displacementPass(self, grid, min, max):
        """
        Takes a square (defined by upper-left and lower-right corners) and
        displaces its center and edge midpoints.  Returns the min and max
        corners of the four component squares.

        """
        minx, miny, minz = min
        maxx, maxy, maxz = max
        ctrx = math.floor(minx + (maxx-minx)/2)
        ctry = math.floor(miny + (maxy-miny)/2)

        if ctrx == minx and ctry == miny:
            return []

        node_ul = grid.get_node_at(min)
        node_ur = grid.get_node_at((maxx, miny, minz))
        node_lr = grid.get_node_at(max)
        node_ll = grid.get_node_at((minx, maxy, minz))

        height_center = (node_ul.contents.height + node_ur.contents.height + node_lr.contents.height + node_ll.contents.height) / 4 + (random.random() - 0.5) * self.scale
        height_left = (node_ul.contents.height + node_ll.contents.height) / 2 + (random.random() - 0.5) * self.scale
        height_right = (node_ur.contents.height + node_lr.contents.height) / 2 + (random.random() - 0.5) * self.scale
        height_top = (node_ul.contents.height + node_ur.contents.height) / 2 + (random.random() - 0.5) * self.scale
        height_bottom = (node_ll.contents.height + node_lr.contents.height) / 2 + (random.random() - 0.5) * self.scale

        left = (minx, ctry, minz)
        right = (maxx, ctry, minz)
        top = (ctrx, miny, minz)
        bottom = (ctrx, maxy, minz)
        center = (ctrx, ctry, minz)

        grid.get_node_at(left).contents.height = height_left
        grid.get_node_at(right).contents.height = height_right
        grid.get_node_at(top).contents.height = height_top
        grid.get_node_at(bottom).contents.height = height_bottom
        grid.get_node_at(center).contents.height = height_center

        return [(min, center),(left, bottom),(center, max),(top, right)]
