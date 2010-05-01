import sys
import string, random
import pygame

from grid import Grid

# intiialize and blank the screen
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Project D.O.R.F.')

viewportX = 0
viewportY = 0

# create the grid, fill it with nodes
gameGrid = Grid()
for x in range(-160,160):
    for y in range(-120,120):
        contents = random.choice(string.letters).upper()
        gameGrid.add_node((x, y, 0), contents)

font_file = pygame.font.match_font('freemono')
font = pygame.font.Font(font_file, 10)
font.set_bold(True)

#for node in gameGrid.nodes():
def updateDisplay():
	screen.fill((0,0,0))
	for x in range(viewportX, viewportX+80):
		for y in range(viewportY, viewportY+60):
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
				viewportY += 1
			if event.key == pygame.K_UP:
				viewportY -= 1
			if event.key == pygame.K_LEFT:
				viewportX -= 1
			if event.key == pygame.K_RIGHT:
				viewportX += 1
			updateDisplay()
	
