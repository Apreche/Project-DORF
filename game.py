import sys
import string, random
import pygame

from grid import Grid
from mover import RandomMover
from terrain import TerrainData
from terrain.generators import MeteorTerrainGenerator, Smoother

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
X_GRID = 320 
Y_GRID = 240
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
DEFAULT_ZOOM = 10 # zoom by changing block size!
FONT_SIZE = 14
ZOOM_INCREMENT = 5
X_SCROLL = 1 
Y_SCROLL = 1

# intialize and blank the screen
pygame.init()
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
pygame.display.set_caption('Project D.O.R.F.')

viewportX = 0
viewportY = 0
viewportZ = 0
zoom = DEFAULT_ZOOM
columns = SCREEN_WIDTH / zoom
rows = SCREEN_HEIGHT / zoom

# create the grid, fill it with nodes
# this is currently a bit slow...
gameGrid = Grid()

for x in range(0, X_GRID):
    for y in range(0 ,Y_GRID):
        terrain = TerrainData()
        gameGrid.add_node((x, y, 0), terrain)

gameGrid.connect_grid()

generator = MeteorTerrainGenerator()
smoother = Smoother(0.5)
generator.apply(gameGrid)
smoother.apply(gameGrid)

font_file = pygame.font.match_font('freemono')
font = pygame.font.Font(font_file, FONT_SIZE)
font.set_bold(True)

movers = []

def rectRender(obj, loc):
    """ Renders a renderable object as a rectangle
        at the given grid square. """
    rectX, rectY, rectZ = loc
    newrectX = (rectX - viewportX) * zoom
    newrectY = (rectY - viewportY) * zoom
    rect = pygame.Rect(newrectX, newrectY, zoom, zoom)
    obj.render(rect, screen)

# updates the screen to show the appropriate visible nodes
def updateDisplay():
    screen.fill((0,0,0))
    for x in range(viewportX, viewportX + columns):
        for y in range(viewportY, viewportY + rows):
            terrainNode = gameGrid.get_node_at((x, y, viewportZ))
            if terrainNode is not None:
                rectRender(terrainNode.contents, terrainNode.location)

    # show current x, y, z in top left corner
    current_view = (viewportX, viewportY, viewportZ, zoom, columns, rows)
    text = font.render(str(current_view), 1, (0, 255, 0))
    rect = text.get_rect()
    rect.x, rect.y = (0,0)
    screen.blit(text, rect)

    displayMovers()

    pygame.display.update()

def moveMovers():
    for mover in movers:
        mover.move()

def isOnScreen(loc):
    x, y, z = loc
    x_on = x >= viewportX and x < viewportX + columns
    y_on = y >= viewportY and y < viewportY + rows
    z_on = z == viewportZ
    return x_on and y_on and z_on

def displayMovers():
    for mover in movers:
        loc = mover.get_location()
        if isOnScreen(loc):
            rectRender(mover, loc)

updateDisplay()

pygame.key.set_repeat(800, 20) # Key repeating

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            locX = x / zoom + viewportX
            locY = y / zoom + viewportY
            loc = (locX, locY, viewportZ)
            if event.button == 1: # Add mover
                rm = RandomMover(gameGrid, (locX, locY, viewportZ))
                movers.append(rm)
            if event.button == 3: # Remove mover
                for mover in movers:
                    if mover.get_location() == loc:
                        movers.remove(mover)
                        break

            updateDisplay()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                viewportY += Y_SCROLL
            if event.key == pygame.K_UP:
                if(viewportY > 0):
                    viewportY -= Y_SCROLL
            if event.key == pygame.K_LEFT:
                if(viewportX > 0):
                    viewportX -= X_SCROLL
            if event.key == pygame.K_RIGHT:
                viewportX += X_SCROLL
            if event.key == pygame.K_PAGEUP:
                viewportZ += 1
            if event.key == pygame.K_PAGEDOWN:
                viewportZ -= 1
            if event.key == pygame.K_z:
                if(zoom + ZOOM_INCREMENT) < 25:
                    zoom += ZOOM_INCREMENT
                    columns = SCREEN_WIDTH / zoom
                    rows = SCREEN_HEIGHT / zoom
            if event.key == pygame.K_x:
                if (zoom - ZOOM_INCREMENT) > 0:
                    zoom -= ZOOM_INCREMENT
                    columns = SCREEN_WIDTH / zoom
                    rows = SCREEN_HEIGHT / zoom
            if event.key == pygame.K_SPACE:
                moveMovers()
                
            updateDisplay()
