from piece import Piece
from constants import SQUARE_WIDTH, RED


def test_piece_move_and_position():
    p = Piece(2, 3, RED)
    # initial coords
    assert p.row == 2 and p.col == 3
    # calc_pos should set x/y based on col/row
    p.calc_pos()
    expected_x = SQUARE_WIDTH * p.col + SQUARE_WIDTH // 2
    expected_y = SQUARE_WIDTH * p.row + SQUARE_WIDTH // 2
    assert p.x == expected_x and p.y == expected_y

    # move updates row/col and recalculates position
    p.move(4, 1)
    assert p.row == 4 and p.col == 1
    assert p.x == SQUARE_WIDTH * 1 + SQUARE_WIDTH // 2


def test_make_king_flag():
    p = Piece(0, 1, RED)
    assert not p.king
    p.make_king()
    assert p.king
