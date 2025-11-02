from checker import GameState, Move
from board import Board
from constants import BLACK, RED


def test_get_all_pieces_returns_correct_color():
    b = Board()
    state = GameState()

    black_pieces = state.get_all_pieces(BLACK, b)
    red_pieces = state.get_all_pieces(RED, b)

    # counts should match initial board counts
    assert len(black_pieces) == 12
    assert len(red_pieces) == 12


def test_get_legal_actions_initial_board():
    b = Board()
    state = GameState()

    actions = state.get_legal_actions(BLACK, b)

    # actions should be a dict mapping piece coords to move lists
    assert isinstance(actions, dict)
    # On the initial board, there should be some legal forward moves for black pieces
    # ensure at least one piece has moves
    has_moves = any(len(moves) > 0 for moves in actions.values())
    assert has_moves


def test_range_and_jump_check():
    b = Board()
    state = GameState()
    # out of range positions
    assert not state.range_check(-1, 0)
    assert not state.range_check(ROWS:=8, 0)  # using ROWS from constants isn't necessary here


def test_copy_board_is_independent():
    b = Board()
    # pick an initial piece
    orig_piece = b.get_piece(2, 1)
    assert orig_piece != 0

    copy = b.deep_copy_board()
    copy_piece = copy.get_piece(2, 1)
    # different object instances
    assert copy_piece is not orig_piece

    # move the piece on the copied board
    copy.move(copy_piece, 4, 4)

    # copied board should reflect the move
    assert copy.get_piece(4, 4) is copy_piece
    assert copy.get_piece(2, 1) == 0

    # original board must remain unchanged
    assert b.get_piece(2, 1) is orig_piece
    assert b.get_piece(4, 4) == 0


def test_generate_successor_capture_and_original_unchanged():
    b = Board()
    gs = GameState()

    # prepare a jump: ensure black at 2,1 and red at 3,2 and empty at 4,3
    from piece import Piece
    # ensure target is empty
    b.set_piece(4, 3, 0)
    # place a red piece at 3,2
    red = Piece(3, 2, RED)
    b.set_piece(3, 2, red)

    start = (2, 1)
    end = (4, 3)
    mv = Move(start=start, end=end)
    orig_piece = b.get_piece(*start)
    succ = gs.generate_successor(b, mv)

    # successor should have piece at end
    p_succ = succ.get_piece(*end)
    assert p_succ != 0
    # captured square should be empty in successor
    assert succ.get_piece(3, 2) == 0

    # original board should be unchanged
    assert b.get_piece(*start) is orig_piece
    assert b.get_piece(3, 2) is red


def test_generate_successor_promotion_and_original_unchanged():
    b = Board()
    gs = GameState()
    from piece import Piece

    # place a red piece just before promotion row
    p = Piece(1, 2, RED)
    b.set_piece(1, 2, p)
    # ensure destination empty
    b.set_piece(0, 1, 0)

    mv = Move(start=(1, 2), end=(0, 1))
    succ = gs.generate_successor(b, mv)

    # successor piece at end should be king
    ps = succ.get_piece(0, 1)
    assert ps != 0 and ps.king

    # original should remain non-king at original pos
    assert b.get_piece(1, 2) is p
    assert not p.king
