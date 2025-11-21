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

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.bmp'), (44, 25))