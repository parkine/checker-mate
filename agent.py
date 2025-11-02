"""
AI Agent for Checkers Game using Minimax Algorithm with Alpha-Beta Pruning

This agent evaluates board positions and selects optimal moves using a
minimax search algorithm. The evaluation function considers multiple factors
including material advantage, king positioning, and board control.
"""

from constants import BLACK, RED, ROWS
from checker import GameState, Move


class Agent:
    """
    AI Agent that plays checkers using minimax algorithm with alpha-beta pruning.

    Attributes:
      color: The color of pieces this agent controls (BLACK or RED)
      depth: How many moves ahead the agent should search (default: 4)
      game_state: GameState instance for move generation and evaluation
    """

    def __init__(self, color, depth=4):
        """
        Initialize the AI agent.

        Args:
          color: The color of pieces this agent controls (BLACK or RED)
          depth: Search depth for minimax algorithm (default: 4)
                 Higher depth = stronger play but slower decisions
                 Recommended range: 3-6
        """
        self.color = color
        self.depth = depth
        self.game_state = GameState()

        # Statistics for analysis (can be logged later)
        self.nodes_explored = 0
        self.pruning_count = 0

    def evaluate(self, board):
        """
        Evaluate the board position from this agent's perspective.

        The evaluation function considers multiple factors:
        1. Material advantage: Count of pieces (normal pieces = 1, kings = 1.5)
        2. Positional advantage: Pieces closer to promotion row are more valuable
        3. King advantage: Kings are more mobile and valuable
        4. Mobility: Number of available moves (more options = better position)

        Args:
          board: The Board object to evaluate

        Returns:
          float: Positive score favors this agent, negative favors opponent
                 Score range typically: -100 to +100
        """
        # Get opponent color
        opponent_color = RED if self.color == BLACK else BLACK

        # Get all pieces for both players
        my_pieces = self.game_state.get_all_pieces(self.color, board)
        opp_pieces = self.game_state.get_all_pieces(opponent_color, board)

        # Material Score: Count pieces with kings worth more
        my_material = 0
        opp_material = 0

        for piece in my_pieces:
            if piece.king:
                my_material += 1.5  # Kings are worth 1.5x regular pieces
            else:
                my_material += 1.0

        for piece in opp_pieces:
            if piece.king:
                opp_material += 1.5
            else:
                opp_material += 1.0

        material_score = (my_material - opp_material) * 10

        # Positional Score: Reward pieces closer to promotion
        positional_score = 0

        for piece in my_pieces:
            if not piece.king:
                if self.color == BLACK:
                    # BLACK moves toward row 7
                    positional_score += piece.row * 0.5
                else:
                    # RED moves toward row 0
                    positional_score += (ROWS - 1 - piece.row) * 0.5

        for piece in opp_pieces:
            if not piece.king:
                if opponent_color == BLACK:
                    positional_score -= piece.row * 0.5
                else:
                    positional_score -= (ROWS - 1 - piece.row) * 0.5

        # King Count: Additional bonus for having kings
        my_kings = sum(1 for p in my_pieces if p.king)
        opp_kings = sum(1 for p in opp_pieces if p.king)
        king_score = (my_kings - opp_kings) * 5

        # Mobility Score: More available moves = better position
        my_moves = self.game_state.get_legal_actions(self.color, board)
        opp_moves = self.game_state.get_legal_actions(opponent_color, board)

        my_move_count = sum(len(moves) for moves in my_moves.values())
        opp_move_count = sum(len(moves) for moves in opp_moves.values())

        mobility_score = (my_move_count - opp_move_count) * 0.5

        # Center Control: Pieces in center squares are more valuable
        center_score = 0
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]

        for piece in my_pieces:
            if (piece.row, piece.col) in center_squares:
                center_score += 2

        for piece in opp_pieces:
            if (piece.row, piece.col) in center_squares:
                center_score -= 2

        # Total evaluation
        total_score = (
            material_score
            + positional_score
            + king_score
            + mobility_score
            + center_score
        )

        return total_score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning for optimal move selection.

        This recursive algorithm explores the game tree to find the best move.
        It assumes both players play optimally and alternates between maximizing
        and minimizing the evaluation score.

        Alpha-beta pruning significantly reduces the number of nodes explored
        by eliminating branches that cannot affect the final decision.

        Args:
          board: Current board state to evaluate
          depth: Remaining search depth (counts down to 0)
          alpha: Best value maximizer can guarantee (used for pruning)
          beta: Best value minimizer can guarantee (used for pruning)
          maximizing_player: True if current player is maximizing, False otherwise

        Returns:
          float: The evaluation score of the best move from this position
        """
        self.nodes_explored += 1

        # Determine current player color based on maximizing/minimizing
        current_color = (
            self.color if maximizing_player else (RED if self.color == BLACK else BLACK)
        )

        # Reached maximum depth
        if depth == 0:
            return self.evaluate(board)

        # Game is over (win, loss, or draw)
        if self.game_state.is_terminal(current_color, board):
            # Heavily reward wins, penalize losses
            if self.game_state.is_win(current_color, board):
                # If it's our agent winning, return large positive value
                return 1000 if current_color == self.color else -1000
            elif self.game_state.is_lose(current_color, board):
                # If it's our agent losing, return large negative value
                return -1000 if current_color == self.color else 1000
            else:
                # Draw
                return 0

        # Get all legal moves for current player
        legal_actions = self.game_state.get_legal_actions(current_color, board)

        # Convert actions dict to list of Move objects
        moves = []
        for start_pos, end_positions in legal_actions.items():
            for end_pos in end_positions:
                moves.append(Move(start=start_pos, end=end_pos))

        if not moves:
            # No legal moves available (should be caught by is_terminal, but safety check)
            return -1000 if maximizing_player else 1000

        if maximizing_player:
            # Maximizing player: try to maximize the score
            max_eval = float("-inf")

            for move in moves:
                successor_board = self.game_state.generate_successor(board, move)

                # Recursively evaluate this move
                eval_score = self.minimax(
                    successor_board, depth - 1, alpha, beta, False
                )

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                # Beta cutoff
                if beta <= alpha:
                    self.pruning_count += 1
                    break

            return max_eval

        else:
            # Minimizing player: try to minimize the score
            min_eval = float("inf")

            for move in moves:
                successor_board = self.game_state.generate_successor(board, move)

                # Recursively evaluate this move
                eval_score = self.minimax(successor_board, depth - 1, alpha, beta, True)

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                # Alpha cutoff
                if beta <= alpha:
                    self.pruning_count += 1
                    break

            return min_eval

    def get_best_move(self, board):
        """
        Select the best move for the current board position using minimax.

        This is the main method called to get the agent's move decision.
        It evaluates all legal moves and returns the one with the best score.

        Args:
          board: Current board state

        Returns:
          Move: The best move to make (Move object with start and end positions)
          float: The evaluation score of the best move

        Returns None, 0 if no legal moves are available.
        """
        # Reset statistics
        self.nodes_explored = 0
        self.pruning_count = 0

        # Get all legal moves
        legal_actions = self.game_state.get_legal_actions(self.color, board)

        # Convert to list of Move objects
        moves = []
        for start_pos, end_positions in legal_actions.items():
            for end_pos in end_positions:
                moves.append(Move(start=start_pos, end=end_pos))

        if not moves:
            return None, 0

        # Evaluate each move using minimax
        best_move = None
        best_score = float("-inf")

        # Initial alpha-beta values
        alpha = float("-inf")
        beta = float("inf")

        for move in moves:
            successor_board = self.game_state.generate_successor(board, move)

            move_score = self.minimax(
                successor_board, self.depth - 1, alpha, beta, False
            )

            if move_score > best_score:
                best_score = move_score
                best_move = move

            alpha = max(alpha, move_score)

        return best_move, best_score

    def get_statistics(self):
        """
        Get statistics about the last move search.

        Returns:
          dict: Dictionary containing nodes_explored and pruning_count
        """
        return {
            "nodes_explored": self.nodes_explored,
            "pruning_count": self.pruning_count,
        }
