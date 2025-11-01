# game.py
import pygame
from constants import *
from board import Board
from piece import Piece

class Game:
  def __init__(self, win):
    self.win = win
    self.selected = None
    self.board = Board()
    self.turn = BLACK

  def select(self, row, col):
    # First click: pick up a piece 
    if self.selected is None:
      piece = self.board.get_piece(row, col)
      if piece == 0:
        return False
      self.selected = piece
      return True

    # Second click: try to move to (row, col)
    moved = self._move(row, col)

    # if move succeeded, advance to next player's turn
    if moved:
      self.switch_turn()

    self.selected = None
    return moved

  def switch_turn(self):
    self.turn = BLACK if self.turn == RED else RED

  def get_current_player(self):
    return self.turn

  def _move(self, row, col):
    piece = self.selected
    if piece is None:
      return False

    # Only allow moves to empty squares 
    if self.board.get_piece(row, col) != 0:
      return False

    # Original coordinates
    r0, c0 = piece.row, piece.col

    # Make a jump
    dr, dc = row - r0, col - c0
    if abs(dr) == 2 and abs(dc) == 2:
      #The middle piece is captured
      mr, mc = (r0 + row) // 2, (c0 + col) // 2
      self.board.set_piece(mr, mc, 0)

    self.board.move(piece, row, col)

    # make it king if it reaches the opposite side 
    if piece.color == RED and row == 0:
      piece.make_king()
    elif piece.color == BLACK and row == ROWS-1:
      piece.make_king()

    return True
  
  #update the display
  def update(self): 
    self.board.draw(self.win) 
    pygame.display.update()
