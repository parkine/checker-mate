from game import Game
from constants import RED, BLACK


def test_starting_player_and_switch():
    g = Game(None)
    assert g.get_current_player() == BLACK
    g.switch_turn()
    assert g.get_current_player() == RED
    g.switch_turn()
    assert g.get_current_player() == BLACK


def test_select_move_toggles_turn():
    g = Game(None)
    start = g.get_current_player()
    assert g.select(2, 1) is True  # pick piece
    moved = g.select(3, 0)  # attempt move
    assert moved is True
    assert g.get_current_player() != start
