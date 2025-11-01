from board import Board
from piece import Piece
from constants import ROWS, COLS, RED, BLACK


def test_board_initial_setup_counts():
    b = Board()
    black_count = 0
    red_count = 0
    for r in range(ROWS):
        for c in range(COLS):
            p = b.get_piece(r, c)
            if p != 0:
                assert isinstance(p, Piece)
                if p.color == BLACK:
                    black_count += 1
                elif p.color == RED:
                    red_count += 1

    # standard checkers starts with 12 pieces per side
    assert black_count == 12
    assert red_count == 12


def test_board_move_and_set_piece():
    b = Board()
    p = b.get_piece(2, 1)
    assert p != 0
    original = b.get_piece(2, 1)
    b.move(original, 3, 0)
    assert b.get_piece(3, 0) is original
    assert b.get_piece(2, 1) == 0

    # set_piece sets a piece and updates its coords
    newp = Piece(0, 0, RED)
    b.set_piece(4, 4, newp)
    assert b.get_piece(4, 4) is newp
    assert newp.row == 4 and newp.col == 4
