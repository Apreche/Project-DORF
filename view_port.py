import math
import pygame

# Zoom values are defined in terms of block size (pixels per grid square)
MIN_BLOCK_SIZE = 4
DEFAULT_BLOCK_SIZE = 10
MAX_BLOCK_SIZE = 40
ZOOM_FACTOR = 1.5 # Multiplicative zoom factor

# Scroll values are defined in terms of number of pixels moved
X_SCROLL = MAX_BLOCK_SIZE
Y_SCROLL = MAX_BLOCK_SIZE

class ViewPort(object):
    """ A class that represents the current view of the game grid. """
    def __init__(self, location, screenRes, gridSize, terrainSurf):
        self.x, self.y, self.z = location
        self.blockSize = DEFAULT_BLOCK_SIZE
        self.screenWidth, self.screenHeight = self.screenRes = screenRes
        self.gridWidth, self.gridHeight = gridSize
        self.columns = self.screenWidth / self.blockSize
        self.rows = self.screenHeight / self.blockSize
        self.terrainSurf = terrainSurf
        self.viewArea = pygame.Surface(self.screenRes)

    def zoom_in(self):
        newBlockSize = int(math.floor(self.blockSize * ZOOM_FACTOR))
        if newBlockSize > MAX_BLOCK_SIZE: newBlockSize = MAX_BLOCK_SIZE
        self.set_block_size(newBlockSize)

    def zoom_out(self):
        newBlockSize = int(math.ceil(self.blockSize / ZOOM_FACTOR))
        if newBlockSize < MIN_BLOCK_SIZE: newBlockSize = MIN_BLOCK_SIZE
        self.set_block_size(newBlockSize)

    def set_block_size(self, newBlockSize):
        """ Change the block size """
        centerX = self.x + self.columns / 2
        centerY = self.y + self.rows / 2
        self.blockSize = newBlockSize
        self.columns = self.screenWidth / self.blockSize
        self.rows = self.screenHeight / self.blockSize
        self.x = centerX - self.columns / 2
        self.y = centerY - self.rows / 2
        self.bound()

    def scroll(self, direction):
        """ Scroll in the given direction """
        deltaX = direction[0] * X_SCROLL / self.blockSize
        deltaY = direction[1] * Y_SCROLL / self.blockSize
        self.x += deltaX
        self.y += deltaY
        self.bound()

    def bound(self):
        """ Keep the grid view bounded """
        if self.x + self.columns > self.gridWidth:
            self.x = self.gridWidth - self.columns
        if self.y + self.rows > self.gridHeight:
            self.y = self.gridHeight - self.rows
        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0

    def contains(self, (x, y, z)):
        """ Returns true if the given grid location is currently visible """
        x_on = x >= self.x and x < self.x + self.columns
        y_on = y >= self.y and y < self.y + self.rows
        z_on = z == self.z
        return x_on and y_on and z_on

    def screen2grid(self, (screenX, screenY)):
        """ Returns the grid co-ordinates associated with the 
        given screen co-ordinates """
        locX = screenX / self.blockSize + self.x
        locY = screenY / self.blockSize + self.y
        return locX, locY, self.z

    def grid2screen(self, (gridX, gridY, gridZ)):
        """ Returns the screen co-ordinates associated with the 
        given grid co-ordinates """
        screenX = (gridX - self.x) * self.blockSize
        screenY = (gridY - self.y) * self.blockSize
        return screenX, screenY

    def render_terrain(self, target):
        """ Renders the viewable terrain onto the given target surface """
        area = pygame.Rect(self.x, self.y, self.columns, self.rows)
        viewArea = self.terrainSurf.subsurface(area)
        pygame.transform.scale(viewArea, self.screenRes, target)

    def __str__(self):
        return str((self.x, self.y, self.z, self.blockSize,
            self.columns, self.rows))
