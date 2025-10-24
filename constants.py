import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_WIDTH = WIDTH // COLS

#piece
RED = (255, 0, 0)
BLACK = (0, 0, 0)
#board
BEIGE = (245, 241, 221)
BROWN = (78,53,36)
# Square outline
GREY = (127, 127, 127)
# Possible moves
BLUE = (0x2878c8)
ORANGE = (0xc87828)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))