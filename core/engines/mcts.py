import math
import random
import time
from typing import List, Optional
from core.game import TicTacToeBoard
from .base import BaseEngine, MoveTelemetry, CandidateMoveEval

class MCTSNode:
    def __init__(self, board: TicTacToeBoard, parent: Optional["MCTSNode"] = None, move: Optional[int] = None, player: str = "O"):
        self.board = board
        self.parent = parent
        self.move = move
        self.player = player
        self.children: List["MCTSNode"] = []
        self.visits = 0
        self.wins = 0.0

    def is_fully_expanded(self) -> bool:
        return len(self.children) == len(self.board.get_legal_moves())

    def ucb1(self, exploration_constant: float = 1.414) -> float:
        if self.visits == 0:
            return float("inf")
        return (self.wins / self.visits) + exploration_constant * math.sqrt(math.log(self.parent.visits) / self.visits)

class MonteCarloTreeSearchEngine(BaseEngine):
    def __init__(self, player_symbol: str = "O", simulations: int = 1500):
        super().__init__(player_symbol)
        self.simulations = simulations

    def select_move(self, board: TicTacToeBoard) -> MoveTelemetry:
        start_time = time.perf_counter()
        root = MCTSNode(board=board, player=self.symbol)
        max_depth = 0

        for _ in range(self.simulations):
            node = root
            depth = 0

            # 1. Selection
            while node.children and node.is_fully_expanded() and not node.board.is_terminal():
                node = max(node.children, key=lambda c: c.ucb1())
                depth += 1

            # 2. Expansion
            if not node.board.is_terminal() and not node.is_fully_expanded():
                legal_moves = node.board.get_legal_moves()
                tried = [c.move for c in node.children]
                untried = [m for m in legal_moves if m not in tried]
                if untried:
                    move = random.choice(untried)
                    next_player = self.opponent_symbol if node.player == self.symbol else self.symbol
                    child_node = MCTSNode(
                        board=node.board.make_move(move, node.player),
                        parent=node,
                        move=move,
                        player=next_player
                    )
                    node.children.append(child_node)
                    node = child_node
                    depth += 1

            max_depth = max(max_depth, depth)

            # 3. Simulation
            sim_board = node.board
            curr_p = node.player
            while not sim_board.is_terminal():
                m = random.choice(sim_board.get_legal_moves())
                sim_board = sim_board.make_move(m, curr_p)
                curr_p = self.opponent_symbol if curr_p == self.symbol else self.symbol

            # 4. Backpropagation
            res = sim_board.get_result(self.symbol)
            score = 1.0 if res == 1.0 else (0.5 if res == 0.0 else 0.0)

            while node is not None:
                node.visits += 1
                node.wins += score
                node = node.parent

        best_child = max(root.children, key=lambda c: c.visits)
        elapsed = (time.perf_counter() - start_time) * 1000.0

        candidates: List[CandidateMoveEval] = []
        for child in root.children:
            wr = child.wins / child.visits if child.visits > 0 else 0.0
            norm_score = (wr - 0.5) * 2.0
            candidates.append(CandidateMoveEval(
                cell_index=child.move,
                score=round(norm_score, 2),
                visits_or_nodes=child.visits,
                rationale=f"{wr*100:.1f}% win/draw rate ({child.visits} rollouts)"
            ))

        candidates.sort(key=lambda x: x.visits_or_nodes, reverse=True)
        discarded_child = candidates[-1] if len(candidates) > 1 else None
        why_disc = ""
        if discarded_child and discarded_child.cell_index != best_child.move:
            why_disc = f"Square {discarded_child.cell_index} was under-sampled ({discarded_child.visits_or_nodes} visits) due to poor UCB1 confidence."

        best_wr = (best_child.wins / best_child.visits) if best_child.visits > 0 else 0.0
        return MoveTelemetry(
            best_move=best_child.move,
            candidate_evaluations=candidates,
            nodes_evaluated=self.simulations,
            max_depth_reached=max_depth,
            pruned_branches=0,
            duration_ms=elapsed,
            confidence_score=round((best_wr - 0.5) * 2.0, 3),
            engine_name="Monte Carlo Tree Search",
            reasoning=f"Identified square {best_child.move} as optimal through {best_child.visits} playout rollouts ({best_wr*100:.1f}% win/draw expectation).",
            why_discarded=why_disc
        )
