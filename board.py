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
        piece = self.get_piece(r, c)
        if piece != 0:
            piece.draw(win)
  
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
  
  def deep_copy_board(self):
    new_board = Board()
    for r in range(ROWS):
        for c in range(COLS):
            cell = self.get_piece(r, c)
            if cell == 0:
                new_board.set_piece(r, c, 0)
            else:
                p = Piece(cell.row, cell.col, cell.color)
                if getattr(cell, 'king', True):
                    p.make_king()
                new_board.set_piece(r, c, p)
    return new_board
  
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
      
