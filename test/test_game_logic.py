from game import Game
from board import Board
from constants import RED, BLACK, ROWS


def test_select_invalid_and_valid_moves():
    g = Game(None)
    # selecting an empty square should return False
    assert g.select(3, 3) is False

    # select a valid black piece and move it
    assert g.select(2, 1) is True
    moved = g.select(3, 0)
    assert moved is True


def test_jump_capture_removes_middle_piece():
    g = Game(None)
    b = g.board
    # set up a simple jump: place a red piece adjacent to a black piece
    # clear two squares and place pieces manually
    b.set_piece(4, 3, 0)
    b.set_piece(3, 2, 0)
    # place black at 2,1 (already exists in initial) and red at 3,2
    # ensure red is at 3,2
    from piece import Piece
    red = Piece(3, 2, RED)
    b.set_piece(3, 2, red)

    # select black at 2,1 and jump to 4,3
    assert g.select(2, 1) is True
    moved = g.select(4, 3)
    assert moved is True
    # middle piece at 3,2 should be removed
    assert b.get_piece(3, 2) == 0


def test_promotion_to_king():
    g = Game(None)
    b = g.board
    # create a red piece that will be promoted by moving to row 0
    from piece import Piece
    p = Piece(1, 2, RED)
    b.set_piece(1, 2, p)

    # ensure target square is empty and it's red's turn
    b.set_piece(0, 1, 0)
    g.turn = RED
    # simulate selecting and moving to row 0
    assert g.select(1, 2) is True
    moved = g.select(0, 1)
    assert moved is True
    assert p.king is True
