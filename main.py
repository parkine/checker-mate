# main.py
import pygame
from board import Board
from constants import *

# Initialize pygame
pygame.init()

# Create the window (same size as your board)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

board = Board()

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    board.draw(WIN)
    pygame.display.update()

pygame.quit()

