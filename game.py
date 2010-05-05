import sys
import pygame

from view_port import ViewPort
from grid import Grid
from mover import RandomMover
from terrain import TerrainData
from terrain.generators import MeteorTerrainGenerator, Smoother, PlasmaFractalGenerator


class Game:
    def __init__(self):
        #Our main variables used within the game
        self.resolution = self.width, self.height = 800, 600
        self.gridSize = self.xGrid, self.yGrid = 320, 240 
        self.movers = []
        self._fontFile = pygame.font.match_font('freemono')
        self._fontSize = 14
       
        #Our main view port/camera
        self.view = ViewPort((0, 0, 0), self.resolution, self.gridSize)

        #Build our main grid
        self.gameGrid = Grid()
        self.make_grid(self.gridSize)
        
        #initialize and blank the screen
        pygame.init()
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption('Project D.O.R.F.')
        pygame.key.set_repeat(800, 20) # Key repeating
        self.font = pygame.font.Font(self._fontFile, self._fontSize)
        self.font.set_bold(True)

        self.generate_terrain() 
        self.updateDisplay()

    def make_grid(self, gridSize):
        for x in range(0, gridSize[0]):
            for y in range(0 ,gridSize[1]):
                terrain = TerrainData()
                self.gameGrid.add_node((x, y, 0), terrain)
        

    def generate_terrain(self):
        generator = PlasmaFractalGenerator(200)
        generator.apply(self.gameGrid)
        self.gameGrid.connect_grid()

        generator = MeteorTerrainGenerator()
        smoother = Smoother(0.5)
        generator.apply(self.gameGrid)
        smoother.apply(self.gameGrid)


    # updates the screen to show the appropriate visible nodes
    def updateDisplay(self):
        self.screen.fill((0,0,0))
        for x in xrange(self.view.x, self.view.x + self.view.columns):
            for y in xrange(self.view.y, self.view.y + self.view.rows):
                loc = (x, y, self.view.z)
                terrainNode = self.gameGrid.get_node_at(loc)
                if terrainNode is not None:
                    screenX, screenY = self.view.grid2screen(loc)
                    rect = pygame.Rect(screenX, screenY,
                            self.view.blockSize, self.view.blockSize)
                    terrainNode.contents.render(rect, self.screen)

        text = self.font.render(str(self.view), 1, (0, 255, 0))
        rect = text.get_rect()
        rect.x, rect.y = (0,0)
        self.screen.blit(text, rect)
        self.displayMovers()

        pygame.display.update()

    def moveMovers(self):
        for mover in self.movers:
            mover.move()

    def displayMovers(self):
        for mover in self.movers:
            loc = mover.get_location()
            if self.view.contains(loc):
                screenX, screenY = self.view.grid2screen(loc)
                rect = pygame.Rect(screenX, screenY,
                         self.view.blockSize, self.view.blockSize)
                mover.render(rect, self.screen)

    def execute(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    loc = self.view.screen2grid(event.pos)
                    if event.button == 1: # Add mover
                        rm = RandomMover(self.gameGrid, loc)
                        self.movers.append(rm)
                    if event.button == 3: # Remove mover
                        for mover in self.movers:
                            if mover.get_location() == loc:
                                self.movers.remove(mover)
                                break

                    self.updateDisplay()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.view.scroll((0, 1))
                    if event.key == pygame.K_UP:
                        self.view.scroll((0, -1))
                    if event.key == pygame.K_LEFT:
                        self.view.scroll((-1, 0))
                    if event.key == pygame.K_RIGHT:
                        self.view.scroll((1, 0))
                    if event.key == pygame.K_PAGEUP:
                        self.view.z += 1
                    if event.key == pygame.K_PAGEDOWN:
                        self.view.z -= 1
                    if event.key == pygame.K_z:
                        self.view.zoom_in()
                    if event.key == pygame.K_x:
                        self.view.zoom_out()
                    if event.key == pygame.K_SPACE:
                        self.moveMovers()
                
                    self.updateDisplay()

if __name__ == "__main__":
    dorf = Game()
    dorf.execute()
