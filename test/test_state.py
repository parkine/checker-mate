from board import Board
from checker import GameState
from agent import Agent
from constants import *

b = Board()
state = GameState()
agent_black = Agent(BLACK, [])

actions = state.get_legal_actions(agent_black, b)
print('Number of pieces with moves:', len(actions))
# print a short summary
for k, v in actions.items():
    print(f'{k} -> {v}')
