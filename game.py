import sys
import pygame

from view_port import ViewPort
from grid import Grid
from mover import RandomMover
from terrain import TerrainData
from terrain.generators import MeteorTerrainGenerator, Smoother

X_GRID = 320 
Y_GRID = 240
GRID_SIZE = (X_GRID, Y_GRID)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

FONT_SIZE = 14

# intialize and blank the screen
pygame.init()
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
pygame.display.set_caption('Project D.O.R.F.')
view = ViewPort((0, 0, 0), SCREEN_RESOLUTION, GRID_SIZE)

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

# updates the screen to show the appropriate visible nodes
def updateDisplay():
    screen.fill((0,0,0))
    for x in xrange(view.x, view.x + view.columns):
        for y in xrange(view.y, view.y + view.rows):
            loc = (x, y, view.z)
            terrainNode = gameGrid.get_node_at(loc)
            if terrainNode is not None:
                screenX, screenY = view.grid2screen(loc)
                rect = pygame.Rect(screenX, screenY,
                        view.blockSize, view.blockSize)
                terrainNode.contents.render(rect, screen)

    # show current x, y, z in top left corner
    text = font.render(str(view), 1, (0, 255, 0))
    rect = text.get_rect()
    rect.x, rect.y = (0,0)
    screen.blit(text, rect)

    displayMovers()

    pygame.display.update()

def moveMovers():
    for mover in movers:
        mover.move()

def displayMovers():
    for mover in movers:
        loc = mover.get_location()
        if view.contains(loc):
            screenX, screenY = view.grid2screen(loc)
            rect = pygame.Rect(screenX, screenY,
                     view.blockSize, view.blockSize)
            mover.render(rect, screen)

updateDisplay()

pygame.key.set_repeat(800, 20) # Key repeating

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            loc = view.screen2grid(event.pos)
            if event.button == 1: # Add mover
                rm = RandomMover(gameGrid, loc)
                movers.append(rm)
            if event.button == 3: # Remove mover
                for mover in movers:
                    if mover.get_location() == loc:
                        movers.remove(mover)
                        break

            updateDisplay()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                view.scroll((0, 1))
            if event.key == pygame.K_UP:
                view.scroll((0, -1))
            if event.key == pygame.K_LEFT:
                view.scroll((-1, 0))
            if event.key == pygame.K_RIGHT:
                view.scroll((1, 0))
            if event.key == pygame.K_PAGEUP:
                view.z += 1
            if event.key == pygame.K_PAGEDOWN:
                view.z -= 1
            if event.key == pygame.K_z:
                view.zoom_in()
            if event.key == pygame.K_x:
                view.zoom_out()
            if event.key == pygame.K_SPACE:
                moveMovers()
                
            updateDisplay()
