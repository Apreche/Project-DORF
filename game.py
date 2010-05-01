import sys
import string, random
import pygame

from grid import Grid

# intiialize and blank the screen
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Project D.O.R.F.')
screen.fill((0,0,0))

# create the grid, fill it with nodes
gameGrid = Grid()
for x in range(0,80):
    for y in range(0,60):
        contents = random.choice(string.letters).upper()
        gameGrid.add_node((x, y, 0), contents)

font_file = pygame.font.match_font('freemono')
font = pygame.font.Font(font_file, 10)
font.set_bold(True)

for node in gameGrid.nodes():
    text = font.render(node.contents, 1, (255, 255, 255))
    rect = text.get_rect()
    rect.x, rect.y, z = node.location
    rect.x *= 10
    rect.y *= 10
    screen.blit(text, rect)

pygame.display.update()

while True:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         sys.exit()
