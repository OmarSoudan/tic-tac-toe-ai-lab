import time
from typing import List
from core.game import TicTacToeBoard
from .base import BaseEngine, MoveTelemetry, CandidateMoveEval

class RuleBasedHeuristicEngine(BaseEngine):
    def select_move(self, board: TicTacToeBoard) -> MoveTelemetry:
        start_time = time.perf_counter()
        legal = board.get_legal_moves()
        evals: List[CandidateMoveEval] = []

        best_move = legal[0]
        best_priority = -999.0
        best_reason = ""

        for move in legal:
            score = 0.0
            reason = "Standard territory claim"

            # Immediate win
            if board.make_move(move, self.symbol).check_winner() == self.symbol:
                score = 100.0
                reason = "Delivers immediate winning strike"
            # Critical block
            elif board.make_move(move, self.opponent_symbol).check_winner() == self.opponent_symbol:
                score = 50.0
                reason = "Blocks immediate opponent victory threat"
            # Center anchor
            elif move == 4:
                score = 25.0
                reason = "Dominates center square to maximize board control"
            # Corner anchor
            elif move in (0, 2, 6, 8):
                score = 10.0
                reason = "Secures perimeter corner anchor"
            else:
                score = 2.0
                reason = "Default open edge positioning"

            evals.append(CandidateMoveEval(
                cell_index=move,
                score=score / 100.0,
                visits_or_nodes=1,
                rationale=reason
            ))

            if score > best_priority:
                best_priority = score
                best_move = move
                best_reason = reason

        evals.sort(key=lambda x: x.score, reverse=True)
        elapsed = (time.perf_counter() - start_time) * 1000.0

        why_disc = ""
        if len(evals) > 1:
            worst = evals[-1]
            why_disc = f"Square {worst.cell_index} was skipped due to low heuristic weight: {worst.rationale}."

        return MoveTelemetry(
            best_move=best_move,
            candidate_evaluations=evals,
            nodes_evaluated=len(legal),
            max_depth_reached=1,
            pruned_branches=0,
            duration_ms=elapsed,
            confidence_score=best_priority / 100.0,
            engine_name="Rule-Based Expert",
            reasoning=f"Selected square {best_move} because it {best_reason.lower()}.",
            why_discarded=why_disc
        )
