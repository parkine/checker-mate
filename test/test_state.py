from board import Board
from checker import GameState
from constants import *

b = Board()
state = GameState()

actions = state.get_legal_actions(BLACK, b)
print('Number of pieces with moves:', len(actions))
# print a short summary
for k, v in actions.items():
    print(f'{k} -> {v}')
