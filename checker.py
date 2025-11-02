from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from constants import *
from board import Board
from piece import Piece

Color = Tuple[int, int, int]

class GameState:
  #return the list of pieces of the agent
  def get_all_pieces(self, color: Color, board: Board) -> list[Piece]:
    pieces = []

    for r in range(ROWS):
      for c in range(COLS):
        p = board.get_piece(r, c)
        if p != 0 and p.color == color:
          pieces.append(p)

    return pieces
  
  #return all available legal action of the agent
  def get_legal_actions(self, color: Color, board: Board) ->list[Move]:
    #black moves top to bottom
    fw = 1 if color == BLACK else -1
    bw = -1 if color == BLACK else 1
    left = -1
    right = 1

    pieces = self.get_all_pieces(color, board)

    actions = []
    for p in pieces:
      r, c = p.row, p.col

      #forward left
      if self.range_check(r + fw, c + left) and board.get_piece(r + fw, c + left) == 0:
        actions.append(Move(start=(r, c), end=(r + fw, c + left)))
      #forward right
      if self.range_check(r + fw, c + right) and board.get_piece(r + fw, c + right) == 0:
        actions.append(Move(start=(r, c), end=(r + fw, c + right)))

      
      # check jumps
      # forward left jump
      mid_r_fl = r + fw
      mid_c_fl = c + left
      mid_p_fl = board.get_piece(mid_r_fl, mid_c_fl) if self.range_check(mid_r_fl, mid_c_fl) else 0
      if self.jump_check(r + (fw * 2), c + (left * 2), p, mid_p_fl) and board.get_piece(r + (fw * 2), c + (left * 2)) == 0:
        actions.append(Move(start=(r, c), end=(r + (fw * 2), c + (left * 2))))

      # forward right jump
      mid_r_fr = r + fw
      mid_c_fr = c + right
      mid_p_fr = board.get_piece(mid_r_fr, mid_c_fr) if self.range_check(mid_r_fr, mid_c_fr) else 0
      if self.jump_check(r + (fw * 2), c + (right * 2), p, mid_p_fr) and board.get_piece(r + (fw * 2), c + (right * 2)) == 0:
        actions.append(Move(start=(r, c), end=(r + (fw * 2), c + (right * 2))))

      if(p.king):
        # backward left
        if self.range_check(r + bw, c + left) and board.get_piece(r + bw, c + left) == 0:
          actions.append(Move(start=(r, c), end=(r + bw, c + left)))
        # backward right
        if self.range_check(r + bw, c + right) and board.get_piece(r + bw, c + right) == 0:
          actions.append(Move(start=(r, c), end=(r + bw, c + right)))

        # backward left jump
        mid_r_bl = r + bw
        mid_c_bl = c + left
        mid_p_bl = board.get_piece(mid_r_bl, mid_c_bl) if self.range_check(mid_r_bl, mid_c_bl) else 0
        if self.jump_check(r + (bw * 2), c + (left * 2), p, mid_p_bl) and board.get_piece(r + (bw * 2), c + (left * 2)) == 0:
          actions.append(Move(start=(r, c), end=(r + (bw * 2), c + (left * 2))))

        # backward right jump
        mid_r_br = r + bw
        mid_c_br = c + right
        mid_p_br = board.get_piece(mid_r_br, mid_c_br) if self.range_check(mid_r_br, mid_c_br) else 0
        if self.jump_check(r + (bw * 2), c + (right * 2), p, mid_p_br) and board.get_piece(r + (bw * 2), c + (right * 2)) == 0:
          actions.append(Move(start=(r, c), end=(r + (bw * 2), c + (right * 2))))

    return actions
  
  #In my turn, if opponent has no pieces left, I win
  def is_win(self, color: Color, board: Board):
    opponent_color = RED if color == BLACK else BLACK
    for r in range(ROWS):
      for c in range(COLS):
        p = board.get_piece(r, c)
        if p != 0 and p.color == opponent_color:
          return False
    return True

  #In my turn, if I have no legal moves, I lose
  def is_lose(self, color: Color, board: Board):
    moves = self.get_legal_actions(color, board)
    # Check if any piece has valid moves
    return len(moves) == 0

  #If the number of kings are the same and no one has won or lost, it's a draw
  def is_draw(self, color: Color, board: Board):
    if(self.is_win(color, board) == False and self.is_lose(color, board) == False):
      opponent_color = RED if color == BLACK else BLACK

      my_pieces = self.get_all_pieces(color, board)
      opp_pieces = self.get_all_pieces(opponent_color, board)

      my_king_count = sum(1 for p in my_pieces if p.king)
      opp_king_count = sum(1 for p in opp_pieces if p.king)

      if my_king_count == opp_king_count and len(my_pieces)-my_king_count == 0 and len(opp_pieces)-opp_king_count == 0:
        return True

  #determine if the game has ended
  def is_terminal(self, color: Color, board: Board):
    return self.is_win(color, board) or self.is_lose(color, board) or self.is_draw(color, board)

  #generate a new board state after applying the move
  def generate_successor(self, board: Board, move: Move) -> Board:
    new_board = board.deep_copy_board()

    sr, sc = move.start
    er, ec = move.end
    p = new_board.get_piece(sr, sc)

    # remove captured pieces (if any)
    if abs(sr-er) == 2 and abs(sc-ec) == 2:
      mid_r = (sr + er) // 2
      mid_c = (sc + ec) // 2
      new_board.set_piece(mid_r, mid_c, 0)

    # perform the move on the copied piece
    new_board.move(p, er, ec)

    # handle promotion to king
    if p.color == RED and er == 0:
      p.make_king()
    elif p.color == BLACK and er == ROWS - 1:
      p.make_king()

    return new_board

  #helper functions
  def range_check(self, row, col):
    return 0 <= col and col < COLS and 0 <= row and row < ROWS 
  
  def jump_check(self, row, col, piece, mid_p):
    return (self.range_check(row, col) and 
            mid_p != 0 and
            piece.color != mid_p.color
            )
  
@dataclass
class Move:
  start: Tuple[int,int]
  end: Tuple[int,int]
      
