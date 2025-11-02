from board import Board
from checker import GameState
from constants import *

b = Board()
state = GameState()

actions = state.get_legal_actions(BLACK, b)
print('Number of black moves:', len(actions))
# print a short summary
for move in actions:
    print(f'{move.start} -> {move.end}')
