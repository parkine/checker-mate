# board.py
import pygame
from constants import *
from piece import Piece

class Board:
  def __init__(self):
      self.board = []
      self.create_board()

  def draw_grid(self, win):
      win.fill(BROWN)
      for r in range(ROWS):
          for c in range(COLS):
              if(c + r) % 2 == 0:
                pygame.draw.rect(win, BEIGE, (r*SQUARE_WIDTH, c*SQUARE_WIDTH, SQUARE_WIDTH,SQUARE_WIDTH))

  def create_board(self):
    for r in range(ROWS):
      self.board.append([])
      for c in range(COLS):
          if (c + r) % 2 == 1:
              if r < 3:
                  self.board[r].append(Piece(r, c, BLACK))
              elif r > 4:
                  self.board[r].append(Piece(r, c, RED))
              else:
                  self.board[r].append(0)
          else:
              self.board[r].append(0)

  def draw(self, win):
      self.draw_grid(win)
      for r in range(ROWS):
          for c in range(COLS):
              piece = self.board[r][c]
              if piece != 0:
                  piece.draw(win)
