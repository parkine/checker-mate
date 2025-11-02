# main.py
import pygame
import time
from constants import *
from game import Game
from agent import Agent
from checker import Move, GameState
from logger import create_logger, LogLevel
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


def run_agent_game(depth=4, log_level=LogLevel.INFO, move_delay=1.0):
    """
    Run AI vs AI game with comprehensive logging.

    Args:
      depth: Search depth for minimax (default: 4)
      log_level: Logging level (INFO, DEBUG, or TRACE)
      move_delay: Delay in seconds between moves for visualization (default: 1.0)
    """
    # Initialize logger
    logger = create_logger(log_level=log_level, log_to_file=True)
    logger.log_game_start(mode="AI vs AI")

    # Initialize game
    clock = pygame.time.Clock()
    game = Game(WIN)
    game_state = GameState()

    # Create AI agents
    agent_black = Agent(BLACK, depth=depth)
    agent_red = Agent(RED, depth=depth)

    logger.info(f"BLACK Agent: Search depth = {depth}")
    logger.info(f"RED Agent: Search depth = {depth}")
    logger.info("")

    # Log initial board
    logger.log_board_state(game.board, "Initial Board State")

    # Game loop
    run = True
    turn_number = 0
    max_turns = 200

    # Track position history for draw by repetition
    position_history = {}

    def get_board_hash(board):
        """Create a hash of the board position for repetition detection"""
        board_str = ""
        for r in range(ROWS):
            for c in range(COLS):
                piece = board.get_piece(r, c)
                if piece == 0:
                    board_str += "."
                elif piece.color == BLACK:
                    board_str += "BK" if piece.king else "B"
                else:
                    board_str += "RK" if piece.king else "R"
        return board_str

    while run and turn_number < max_turns:
        clock.tick(FPS)

        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                logger.info("Game terminated by user")
                break

        if not run:
            break

        turn_number += 1
        current_color = game.get_current_player()
        current_agent = agent_black if current_color == BLACK else agent_red

        # Log turn start
        logger.log_turn_start(turn_number, current_color, current_agent)

        # Check for game termination
        if game_state.is_terminal(current_color, game.board):
            if game_state.is_win(current_color, game.board):
                winner = current_color
                reason = "Opponent has no pieces remaining"
                logger.log_game_end(winner, reason)
                break
            elif game_state.is_lose(current_color, game.board):
                winner = RED if current_color == BLACK else BLACK
                reason = "Current player has no legal moves"
                logger.log_game_end(winner, reason)
                break
            elif game_state.is_draw(current_color, game.board):
                logger.log_game_end(winner=None, reason="Draw - equal king count")
                break

        # Get legal moves
        legal_actions = game_state.get_legal_actions(current_color, game.board)
        logger.log_legal_moves(legal_actions, current_color)

        # Check if agent has any moves
        total_moves = sum(len(moves) for moves in legal_actions.values())
        if total_moves == 0:
            winner = RED if current_color == BLACK else BLACK
            logger.log_game_end(winner, "Current player has no legal moves")
            break

        # AI makes decision
        logger.debug("AI is thinking...")
        move_start_time = time.time()
        best_move, score = current_agent.get_best_move(game.board)
        move_end_time = time.time()

        if best_move is None:
            winner = RED if current_color == BLACK else BLACK
            logger.log_game_end(winner, "AI could not find a valid move")
            break

        # Log AI decision
        stats = current_agent.get_statistics()
        logger.log_ai_decision(current_agent, best_move, score, stats)
        logger.log_move_time(move_end_time - move_start_time)

        # Execute move
        start_row, start_col = best_move.start
        end_row, end_col = best_move.end

        # Check if it's a jump
        is_jump = abs(start_row - end_row) == 2

        # Select piece and move it
        game.selected = game.board.get_piece(start_row, start_col)
        moved = game._move(end_row, end_col)

        if not moved:
            logger.log_error(
                f"Failed to execute move {best_move.start} -> {best_move.end}"
            )
            break

        # Check for promotion
        piece = game.board.get_piece(end_row, end_col)
        is_promotion = (
            piece != 0
            and piece.king
            and (
                (current_color == BLACK and end_row == ROWS - 1)
                or (current_color == RED and end_row == 0)
            )
        )

        # Log move execution
        logger.log_move_execution(best_move, current_color, is_jump, is_promotion)

        # Update display
        game.update()
        pygame.display.update()

        # Log board state after move
        logger.log_board_state(game.board, f"Board After Turn {turn_number}")

        # Check for position repetition (threefold repetition = draw)
        board_hash = get_board_hash(game.board)
        position_history[board_hash] = position_history.get(board_hash, 0) + 1

        if position_history[board_hash] >= 3:
            logger.info(
                f"Position repeated {position_history[board_hash]} times - Draw by repetition"
            )
            logger.log_game_end(winner=None, reason="Draw by threefold repetition")
            break

        # Switch turn
        game.switch_turn()

        # Delay for visualization
        time.sleep(move_delay)

    # Check if max turns reached
    if turn_number >= max_turns:
        logger.log_game_end(winner=None, reason=f"Maximum turns ({max_turns}) reached")

    # Keep window open to see final state
    logger.info("")
    logger.info("Game complete. Close window to exit.")

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
        game.update()
        pygame.display.update()
        clock.tick(FPS)

    # Close logger
    logger.close()
    pygame.quit()


def main():
    parser = argparse.ArgumentParser(description="Checker Game with AI Agents")
    parser.add_argument(
        "--mode",
        choices=["human", "agent"],
        default="human",
        help="Choose who plays: human, or agent",
    )
    parser.add_argument(
        "--depth", type=int, default=4, help="Search depth for AI agents (default: 4)"
    )
    parser.add_argument(
        "--log-level",
        choices=["INFO", "DEBUG", "TRACE"],
        default="INFO",
        help="Logging level (default: INFO)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay in seconds between AI moves (default: 1.0)",
    )
    args = parser.parse_args()

    if args.mode == "human":
        print("Running in human vs human mode")
        run_human_game()
    elif args.mode == "agent":
        # Convert log level string to LogLevel constant
        log_level_map = {
            "INFO": LogLevel.INFO,
            "DEBUG": LogLevel.DEBUG,
            "TRACE": LogLevel.TRACE,
        }
        log_level = log_level_map[args.log_level]

        print(f"Running AI vs AI mode")
        print(f"  Search depth: {args.depth}")
        print(f"  Log level: {args.log_level}")
        print(f"  Move delay: {args.delay}s")
        print()

        run_agent_game(depth=args.depth, log_level=log_level, move_delay=args.delay)


main()
