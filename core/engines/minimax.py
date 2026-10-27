import time
from typing import Dict, Tuple, Optional, List
from core.game import TicTacToeBoard
from .base import BaseEngine, MoveTelemetry, CandidateMoveEval

class AlphaBetaEngine(BaseEngine):
    def __init__(self, player_symbol: str = "O", use_pruning: bool = True):
        super().__init__(player_symbol)
        self.use_pruning = use_pruning
        self.transposition_table: Dict[Tuple[Optional[str], ...], float] = {}

    def select_move(self, board: TicTacToeBoard) -> MoveTelemetry:
        start_time = time.perf_counter()
        nodes_evaluated = 0
        pruned_count = 0
        max_depth = 0

        legal_moves = board.get_legal_moves()
        candidate_evals: List[CandidateMoveEval] = []

        best_score = float("-inf")
        best_move = legal_moves[0]
        alpha = float("-inf")
        beta = float("inf")

        for move in legal_moves:
            next_board = board.make_move(move, self.symbol)
            score, nodes, depth, pruned = self._min_value(next_board, alpha, beta, 1)

            nodes_evaluated += nodes + 1
            pruned_count += pruned
            max_depth = max(max_depth, depth)

            if score > 0:
                rat = "Forced Win"
            elif score == 0:
                rat = "Draw Equilibrium"
            else:
                rat = "Leads to Opponent Win"

            candidate_evals.append(CandidateMoveEval(
                cell_index=move,
                score=score,
                visits_or_nodes=nodes,
                rationale=rat
            ))

            if score > best_score:
                best_score = score
                best_move = move

            if self.use_pruning:
                alpha = max(alpha, best_score)

        elapsed = (time.perf_counter() - start_time) * 1000.0
        engine_label = "Alpha-Beta Pruning" if self.use_pruning else "Pure Minimax"

        # Construct analytical justification
        suboptimal = [c for c in candidate_evals if c.cell_index != best_move]
        suboptimal.sort(key=lambda x: x.score, reverse=True)

        if best_score > 0:
            primary_reason = f"Selected square {best_move} because it secures a guaranteed win within {max_depth} plies."
        elif best_score == 0:
            primary_reason = f"Selected square {best_move} to preserve dynamic game-theoretic equilibrium (forced draw)."
        else:
            primary_reason = f"Selected square {best_move} as a defensive delay; all alternate paths concede an immediate win."

        discard_summary = ""
        if suboptimal:
            worst = suboptimal[-1]
            discard_summary = f"Square {worst.cell_index} was discarded because its subtree evaluation yielded {worst.score:+.1f} ({worst.rationale})."

        return MoveTelemetry(
            best_move=best_move,
            candidate_evaluations=candidate_evals,
            nodes_evaluated=nodes_evaluated,
            max_depth_reached=max_depth,
            pruned_branches=pruned_count,
            duration_ms=elapsed,
            confidence_score=best_score,
            engine_name=engine_label,
            reasoning=primary_reason,
            why_discarded=discard_summary,
            extra_stats={"memoized_positions": len(self.transposition_table)}
        )

    def _max_value(self, board: TicTacToeBoard, alpha: float, beta: float, depth: int) -> Tuple[float, int, int, int]:
        if board.is_terminal():
            return board.get_result(self.symbol), 1, depth, 0

        state_key = board.state
        if state_key in self.transposition_table:
            return self.transposition_table[state_key], 1, depth, 0

        v = float("-inf")
        nodes = 1
        max_d = depth
        pruned = 0

        for move in board.get_legal_moves():
            score, n, d, p = self._min_value(board.make_move(move, self.symbol), alpha, beta, depth + 1)
            nodes += n
            pruned += p
            max_d = max(max_d, d)
            v = max(v, score)

            if self.use_pruning:
                if v >= beta:
                    pruned += 1
                    break
                alpha = max(alpha, v)

        self.transposition_table[state_key] = v
        return v, nodes, max_d, pruned

    def _min_value(self, board: TicTacToeBoard, alpha: float, beta: float, depth: int) -> Tuple[float, int, int, int]:
        if board.is_terminal():
            return board.get_result(self.symbol), 1, depth, 0

        state_key = board.state
        if state_key in self.transposition_table:
            return self.transposition_table[state_key], 1, depth, 0

        v = float("inf")
        nodes = 1
        max_d = depth
        pruned = 0

        for move in board.get_legal_moves():
            score, n, d, p = self._max_value(board.make_move(move, self.opponent_symbol), alpha, beta, depth + 1)
            nodes += n
            pruned += p
            max_d = max(max_d, d)
            v = min(v, score)

            if self.use_pruning:
                if v <= alpha:
                    pruned += 1
                    break
                beta = min(beta, v)

        self.transposition_table[state_key] = v
        return v, nodes, max_d, pruned
