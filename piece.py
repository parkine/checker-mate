# piece.py
import pygame
from constants import *

class Piece:

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_WIDTH * self.col + SQUARE_WIDTH // 2
        self.y = SQUARE_WIDTH * self.row + SQUARE_WIDTH // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_WIDTH//2.5
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
