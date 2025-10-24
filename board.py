# board.py
import pygame
from constants import *
from piece import Piece

class Board:
  def __init__(self):
    self.board = []
    self.create_board()
    self.selected = (None, None)

  def draw_grid(self, win):
    win.fill(BROWN)
    for r in range(ROWS):
      for c in range(COLS):
        if(c + r) % 2 == 0:
          pygame.draw.rect(win, BEIGE, (r*SQUARE_WIDTH, c*SQUARE_WIDTH, SQUARE_WIDTH, SQUARE_WIDTH))

  #The board's index: left top corner = (0,0) && right bottom = (7,7)
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
        if self.selected[0] == r and self.selected[1] == c :
          pygame.draw.rect(win, GREY, (c*SQUARE_WIDTH, r*SQUARE_WIDTH, SQUARE_WIDTH, SQUARE_WIDTH), 8)
        piece = self.board[r][c]
        if piece != 0:
            piece.draw(win)

  def select(self, row, col) :
    if self.selected == (row, col) :
      self.selected = (None, None)
    else :
      self.selected = (row, col)
  
  def move(self, piece, row, col):
    self.board[piece.row][piece.col] = 0
    self.board[row][col] = piece
    piece.move(row, col)
    
  def set_piece(self, row, col, piece):
    self.board[row][col] = piece
    if piece != 0:
       piece.move(row, col)

  def get_piece(self, row, col):
    return self.board[row][col]
  
  def debug_print_board(self):
    for rr in self.board.board:
      for cc in rr:
        if cc == 0:
          print(0, end=" ")
        else:
          # show 'R'/'B' and 'K' for king
          tag = "R" if cc.color == (255, 0, 0) else "B"
          if getattr(cc, "king", False):
              tag += "K"
          print(tag, end=" ")
      print()
      
