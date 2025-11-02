"""
Comprehensive Logging System for Checkers AI Game

Provides multi-level logging (INFO, DEBUG, TRACE) with both console
and file output. Logs game events, AI decision-making, board states,
and performance statistics.
"""

import os
import sys
from datetime import datetime
from typing import Optional
from constants import BLACK, RED, ROWS, COLS

class LogLevel:
    """Log level constants"""
    TRACE = 0  # Most verbose - all details
    DEBUG = 1  # Debug information - AI search details
    INFO = 2   # Important events - turns, moves, game events
    NONE = 3   # No logging

class GameLogger:
    """
    Comprehensive logging system for checkers game.

    Supports multiple log levels and outputs to both console and file.
    """

    def __init__(self, log_level=LogLevel.INFO, log_to_file=True, log_dir="logs"):
        """
        Initialize the logger.

        Args:
            log_level: Minimum level to log (TRACE, DEBUG, INFO, or NONE)
            log_to_file: Whether to write logs to a file
            log_dir: Directory to store log files
        """
        self.log_level = log_level
        self.log_to_file = log_to_file
        self.log_dir = log_dir
        self.log_file = None
        self.file_handle = None

        # Statistics tracking
        self.turn_count = 0
        self.total_nodes_explored = 0
        self.total_pruning_count = 0
        self.move_times = []

        # Initialize file logging
        if self.log_to_file:
            self._setup_log_file()

    def _setup_log_file(self):
        """Create logs directory and log file with timestamp"""
        # Create logs directory if it doesn't exist
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f"game_{timestamp}.log")

        try:
            self.file_handle = open(self.log_file, 'w', encoding='utf-8')
            self._write_to_file("=" * 80)
            self._write_to_file(f"CHECKERS AI GAME LOG - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self._write_to_file("=" * 80)
            self._write_to_file("")
        except IOError as e:
            print(f"Warning: Could not create log file: {e}")
            self.log_to_file = False

    def _write_to_file(self, message):
        """Write message to log file"""
        if self.file_handle:
            self.file_handle.write(message + "\n")
            self.file_handle.flush()

    def _log(self, level, message, to_console=True, to_file=True):
        """
        Internal logging method.

        Args:
            level: Log level of this message
            message: Message to log
            to_console: Whether to print to console
            to_file: Whether to write to file
        """
        if level < self.log_level:
            return

        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # Level labels
        level_labels = {
            LogLevel.TRACE: "TRACE",
            LogLevel.DEBUG: "DEBUG",
            LogLevel.INFO: "INFO "
        }
        level_label = level_labels.get(level, "     ")

        formatted_message = f"[{timestamp}] [{level_label}] {message}"

        # Console output
        if to_console:
            print(formatted_message)

        # File output
        if to_file and self.log_to_file:
            self._write_to_file(formatted_message)

    def trace(self, message):
        """Log TRACE level message (most verbose)"""
        self._log(LogLevel.TRACE, message)

    def debug(self, message):
        """Log DEBUG level message"""
        self._log(LogLevel.DEBUG, message)

    def info(self, message):
        """Log INFO level message"""
        self._log(LogLevel.INFO, message)

    def separator(self, char="-", length=80):
        """Print a separator line"""
        self._log(LogLevel.INFO, char * length)

    def section_header(self, title):
        """Print a section header"""
        self.separator("=")
        self.info(f"  {title}")
        self.separator("=")

    # Game Event Logging Methods

    def log_game_start(self, mode="AI vs AI"):
        """Log game initialization"""
        self.section_header("GAME START")
        self.info(f"Mode: {mode}")
        self.info(f"Board Size: {ROWS}x{COLS}")
        self.info("")

    def log_turn_start(self, turn_number, player_color, agent=None):
        """
        Log the start of a turn.

        Args:
            turn_number: Current turn number
            player_color: Color of current player (BLACK or RED)
            agent: Agent object (optional, for AI turns)
        """
        self.turn_count = turn_number

        color_name = "BLACK" if player_color == BLACK else "RED"
        player_type = "AI" if agent else "Human"

        self.separator()
        self.info(f"TURN {turn_number} - {color_name} ({player_type})")
        self.separator()

        if agent:
            self.debug(f"  Agent search depth: {agent.depth}")

    def log_board_state(self, board, label="Current Board State"):
        """
        Log the current board state in a readable format.

        Args:
            board: Board object to log
            label: Label for this board state
        """
        if self.log_level > LogLevel.DEBUG:
            return

        self.debug(f"{label}:")
        self.debug("")

        # Column headers
        header = "    " + "  ".join(str(i) for i in range(COLS))
        self.debug(header)
        self.debug("  " + "-" * (COLS * 3 + 1))

        # Board rows
        for r in range(ROWS):
            row_str = f"{r} | "
            for c in range(COLS):
                piece = board.get_piece(r, c)
                if piece == 0:
                    # Empty square - show board pattern
                    if (r + c) % 2 == 0:
                        row_str += " . "  # Light square
                    else:
                        row_str += "   "  # Dark square (playable)
                else:
                    # Show piece
                    if piece.color == RED:
                        symbol = "R" if not piece.king else "RK"
                    else:
                        symbol = "B" if not piece.king else "BK"
                    row_str += f"{symbol:>2} "

            self.debug(row_str)

        self.debug("")

    def log_legal_moves(self, legal_actions, color):
        """
        Log all legal moves available.

        Args:
            legal_actions: Dictionary of legal actions {(row, col): [(end_row, end_col), ...]}
            color: Color of player making moves
        """
        if self.log_level > LogLevel.DEBUG:
            return

        color_name = "BLACK" if color == BLACK else "RED"

        total_moves = sum(len(moves) for moves in legal_actions.values())
        self.debug(f"Legal moves for {color_name}: {total_moves} available")

        if self.log_level <= LogLevel.TRACE:
            for start_pos, end_positions in legal_actions.items():
                if end_positions:
                    self.trace(f"  From {start_pos}: {end_positions}")

    def log_move_evaluation(self, move, score, depth=None):
        """
        Log evaluation of a specific move.

        Args:
            move: Move object being evaluated
            score: Evaluation score
            depth: Search depth (optional)
        """
        if self.log_level > LogLevel.TRACE:
            return

        depth_str = f" (depth {depth})" if depth else ""
        self.trace(f"  Evaluating move {move.start} -> {move.end}: score = {score:.2f}{depth_str}")

    def log_ai_decision(self, agent, best_move, score, stats):
        """
        Log AI's final move decision with reasoning.

        Args:
            agent: Agent that made the decision
            best_move: Selected Move object
            score: Evaluation score of the move
            stats: Dictionary with 'nodes_explored' and 'pruning_count'
        """
        color_name = "BLACK" if agent.color == BLACK else "RED"

        self.info(f"AI Decision ({color_name}):")
        self.info(f"  Selected Move: {best_move.start} -> {best_move.end}")
        self.info(f"  Evaluation Score: {score:.2f}")

        self.debug(f"  Search Statistics:")
        self.debug(f"    Nodes Explored: {stats['nodes_explored']}")
        self.debug(f"    Branches Pruned: {stats['pruning_count']}")

        # Calculate pruning efficiency
        if stats['nodes_explored'] > 0:
            efficiency = (stats['pruning_count'] / stats['nodes_explored']) * 100
            self.debug(f"    Pruning Efficiency: {efficiency:.1f}%")

        # Update global statistics
        self.total_nodes_explored += stats['nodes_explored']
        self.total_pruning_count += stats['pruning_count']

        self.info("")

    def log_move_execution(self, move, color, is_jump=False, is_promotion=False):
        """
        Log execution of a move.

        Args:
            move: Move object being executed
            color: Color of piece moving
            is_jump: Whether this move captures an opponent piece
            is_promotion: Whether this move promotes to king
        """
        color_name = "BLACK" if color == BLACK else "RED"

        move_type = "JUMP" if is_jump else "MOVE"
        self.info(f"Executing {move_type}: {color_name} piece from {move.start} to {move.end}")

        if is_jump:
            mid_r = (move.start[0] + move.end[0]) // 2
            mid_c = (move.start[1] + move.end[1]) // 2
            self.info(f"  Captured opponent piece at ({mid_r}, {mid_c})")

        if is_promotion:
            self.info(f"  PROMOTION: Piece became a KING!")

        self.info("")

    def log_game_end(self, winner, reason):
        """
        Log game ending.

        Args:
            winner: Color of winner (BLACK, RED, or None for draw)
            reason: Reason for game end (e.g., "No legal moves", "No pieces remaining")
        """
        self.separator("=")
        self.info("GAME OVER")
        self.separator("=")

        if winner is None:
            self.info("Result: DRAW")
        else:
            winner_name = "BLACK" if winner == BLACK else "RED"
            self.info(f"Winner: {winner_name}")

        self.info(f"Reason: {reason}")
        self.info(f"Total Turns: {self.turn_count}")

        self.separator()
        self.log_game_statistics()

    def log_game_statistics(self):
        """Log overall game statistics"""
        self.info("Game Statistics:")
        self.info(f"  Total Turns: {self.turn_count}")
        self.info(f"  Total Nodes Explored: {self.total_nodes_explored}")
        self.info(f"  Total Branches Pruned: {self.total_pruning_count}")

        if self.total_nodes_explored > 0:
            overall_efficiency = (self.total_pruning_count / self.total_nodes_explored) * 100
            self.info(f"  Overall Pruning Efficiency: {overall_efficiency:.1f}%")

        if self.move_times:
            avg_time = sum(self.move_times) / len(self.move_times)
            self.info(f"  Average Time per Move: {avg_time:.3f}s")
            self.info(f"  Total Game Time: {sum(self.move_times):.2f}s")

        self.separator("=")

    def log_error(self, error_message):
        """Log an error message"""
        self._log(LogLevel.INFO, f"ERROR: {error_message}")

    def log_move_time(self, time_seconds):
        """
        Track time taken for a move.

        Args:
            time_seconds: Time in seconds
        """
        self.move_times.append(time_seconds)
        self.debug(f"Move computation time: {time_seconds:.3f}s")

    def close(self):
        """Close the log file"""
        log_file_path = self.log_file

        if self.file_handle:
            self._write_to_file("")
            self._write_to_file("=" * 80)
            self._write_to_file(f"LOG CLOSED - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self._write_to_file("=" * 80)
            self.file_handle.close()
            self.file_handle = None

        if log_file_path:
            print(f"Log file saved to: {log_file_path}")

def create_logger(log_level=LogLevel.INFO, log_to_file=True, log_dir="logs"):
    """
    Create a GameLogger instance.

    Args:
        log_level: LogLevel.TRACE, LogLevel.DEBUG, LogLevel.INFO, or LogLevel.NONE
        log_to_file: Whether to save logs to file
        log_dir: Directory for log files

    Returns:
        GameLogger instance
    """
    return GameLogger(log_level, log_to_file, log_dir)
