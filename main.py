# main.py
import pygame
from constants import *
from game import Game
import argparse

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
  x, y = pos
  row = y // SQUARE_WIDTH
  col = x // SQUARE_WIDTH
  return row, col

def run_human_game():
  run = True
  clock = pygame.time.Clock()
  game = Game(WIN)

  while run:
    clock.tick(FPS)

    # if game.winner() != None:
    #     print(game.winner())
    #     run = False

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = get_row_col_from_mouse(pos)
        game.select(row, col)

    game.update()

  pygame.quit()

def run_agent_game():
   return

def main():
    parser = argparse.ArgumentParser(description="Checker Game with AI Agents")
    parser.add_argument("--mode", choices=["human", "agent"], default="human",
                        help="Choose who plays: human, or agent")
    args = parser.parse_args()

    if args.mode == "human":
        print("Running in human vs human mode")
        run_human_game()
    elif args.mode == "agent":
        print("Running human vs AI mode")
        run_agent_game()

main()
