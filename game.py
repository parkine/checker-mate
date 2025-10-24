# game.py
import pygame
from constants import *
from board import Board
from piece import Piece

# game.py (only the select/_move parts shown)

class Game:
  def __init__(self, win):
    self.win = win
    self.selected = None
    self.board = Board()
    self.turn = BLACK
    self.valid_moves = set()

  def select(self, row, col):
    # First click: pick up a piece 
    if self.selected is None:
      self.board.select(row, col)
      piece = self.board.get_piece(row, col)
      if piece == 0:
        return False
      self.selected = piece
      # Update valid moves attribute
      self.get_valid_moves(piece.row, piece.col)
      return True

    # Second click: try to move to (row, col)
    moved = self._move(row, col)
    
    self.selected = None
    self.board.selected = (None, None)
    self.valid_moves = set()
    return moved

  def _move(self, row, col):
    piece = self.selected
    if piece is None:
      return False

    # Piece has to match player color
    if piece.color != self.turn :
        return False

    # Only allow moves to empty squares 
    #if self.board.get_piece(row, col) != 0:
      #return False

    # Only allow valid moves
    if (row, col) not in self.valid_moves :
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

    # Change player turn
    if self.turn == RED :
      self.turn = BLACK
    elif self.turn == BLACK :
      self.turn = RED

    return True
  
  #update the display
  def update(self): 
    self.board.draw(self.win)
    for x in self.valid_moves :
      row, col = x
      pygame.draw.circle(self.win, BLUE, (col * SQUARE_WIDTH + SQUARE_WIDTH // 2, row * SQUARE_WIDTH + SQUARE_WIDTH // 2), 8)
    pygame.display.update()


  # Finds single-jump valid moves
  def get_valid_moves(self, row, col) :

    # Disallow wrong turn selection
    if self.board.get_piece(row, col).color != self.turn :
      self.valid_moves = []
      return False

    # Empty is_valid
    self.is_valid = []

    # Get piece
    piece = self.board.get_piece(row, col)

    # List of possible moves
    to_check = []

    # Check forward or back diagonals for empty, or opponent color
    # If Red or King, Up
    if ((piece.color == RED) or (piece.king)) and (row - 1 >= 0) :
      # Up-right
      if (col + 1 < COLS) :
        to_check.append((row - 1, col + 1))
      # Up-left
      if (col - 1 >= 0) :
        to_check.append((row - 1, col - 1))

    # If Black or King, Down
    if ((piece.color == BLACK) or (piece.king)) and (row + 1 < ROWS) :
      # Down-right
      if (col + 1 < COLS) :
        to_check.append((row + 1, col + 1))
      # Down-left
      if (col - 1 >= 0) :
        to_check.append((row + 1, col - 1))
      
    # Check for empty, or opponent; check empty on jump over opponent
    for x in to_check :
      # Position empty
      if (self.board.get_piece(x[0], x[1]) == 0) :
        # Add it to the move list
        self.valid_moves.add((x[0], x[1]))
      # Position is opponent
      elif (self.board.get_piece(x[0], x[1]).color != piece.color) :
        # Get jump coordinates (BUT I CANNAE CAPN!!!)
        tmp_row = (x[0] - row) * 2 + row
        tmp_col = (x[1] - col) * 2 + col
        # Check if in-bounds
        if ((tmp_row or tmp_col) < 0) or (tmp_row >= ROWS) or (tmp_col >= COLS) :
          break
        # Check if no piece on that position
        if (self.board.get_piece(tmp_row, tmp_col) != 0) :
          break;
        self.valid_moves.add((tmp_row, tmp_col))
