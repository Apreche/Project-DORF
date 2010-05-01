import sys
import string, random
import pygame

from grid import Grid
from terrain import TerrainData, MeteorTerrainGenerator

# intiialize and blank the screen
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Project D.O.R.F.')

viewportX = 0
viewportY = 0

# create the grid, fill it with nodes
# this is currently a bit slow...
gameGrid = Grid()
for x in range(-160,160):
    for y in range(-120,120):
        # uncomment these two if you want random letters back
		#contents = random.choice(string.letters).upper()
        #gameGrid.add_node((x, y, 0), contents)
        terrain = TerrainData()
        #terrain.randomize()
        gameGrid.add_node((x, y, -1), terrain)

#gameGrid.connect_grid()

generator = MeteorTerrainGenerator()
generator.apply(gameGrid)

font_file = pygame.font.match_font('freemono')
font = pygame.font.Font(font_file, 10)
font.set_bold(True)

# updates the screen to show the appropriate visible nodes
def updateDisplay():
	screen.fill((0,0,0))
	for x in range(viewportX, viewportX+80):
		for y in range(viewportY, viewportY+60):
			terrainNode = gameGrid.get_node_at((x, y, -1))
			if terrainNode != None:
				rect = pygame.Rect((terrainNode.location[0] - viewportX)*10, (terrainNode.location[1] - viewportY)*10, 10, 10)
				terrainNode.contents.render(rect, screen)

			node = gameGrid.get_node_at((x, y, 0))
			if node != None:
				text = font.render(node.contents, 1, (255, 255, 255))
				rect = text.get_rect()
				rect.x, rect.y, z = node.location
				rect.x -= viewportX
				rect.y -= viewportY
				rect.x *= 10
				rect.y *= 10
				screen.blit(text, rect)
				
			
	pygame.display.update()

updateDisplay()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				viewportY += 3
			if event.key == pygame.K_UP:
				viewportY -= 3
			if event.key == pygame.K_LEFT:
				viewportX -= 3
			if event.key == pygame.K_RIGHT:
				viewportX += 3
			updateDisplay()
	
