import random
import time
from core.game import TicTacToeBoard
from .base import BaseEngine, MoveTelemetry

class RandomEngine(BaseEngine):
    """Uniformly samples random legal positions."""
    def select_move(self, board: TicTacToeBoard) -> MoveTelemetry:
        start_time = time.perf_counter()
        legal = board.get_legal_moves()
        move = random.choice(legal)
        elapsed = (time.perf_counter() - start_time) * 1000.0

        return MoveTelemetry(
            best_move=move,
            nodes_evaluated=1,
            max_depth_reached=1,
            pruned_branches=0,
            duration_ms=elapsed,
            confidence_score=0.0,
            engine_name="Random Heuristic",
            reasoning="Selected uniformly at random from remaining legal cells."
        )