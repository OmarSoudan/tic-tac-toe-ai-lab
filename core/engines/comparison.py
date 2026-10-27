import time
from typing import Dict, Any, Type
from core.game import TicTacToeBoard
from core.engines import BaseEngine

class HeadToHeadBenchmark:
    @staticmethod
    def run_matchup(
        engine_a_factory: Any,
        engine_b_factory: Any,
        name_a: str,
        name_b: str,
        rounds: int = 20
    ) -> Dict[str, Any]:
        results = {
            "name_a": name_a,
            "name_b": name_b,
            "rounds": rounds,
            "a_wins": 0,
            "b_wins": 0,
            "draws": 0,
            "avg_latency_a_ms": 0.0,
            "avg_latency_b_ms": 0.0,
            "total_nodes_a": 0,
            "total_nodes_b": 0,
        }

        latencies_a = []
        latencies_b = []

        for r in range(rounds):
            # Alternate who plays 'X' (moves first)
            if r % 2 == 0:
                eng_x = engine_a_factory("X")
                eng_o = engine_b_factory("O")
                is_a_x = True
            else:
                eng_x = engine_b_factory("X")
                eng_o = engine_a_factory("O")
                is_a_x = False

            board = TicTacToeBoard()
            current_sym = "X"

            while not board.is_terminal():
                active_eng = eng_x if current_sym == "X" else eng_o
                t = active_eng.select_move(board)

                if (current_sym == "X" and is_a_x) or (current_sym == "O" and not is_a_x):
                    latencies_a.append(t.duration_ms)
                    results["total_nodes_a"] += t.nodes_evaluated
                else:
                    latencies_b.append(t.duration_ms)
                    results["total_nodes_b"] += t.nodes_evaluated

                board = board.make_move(t.best_move, current_sym)
                current_sym = "O" if current_sym == "X" else "X"

            winner = board.check_winner()
            if winner is None:
                results["draws"] += 1
            elif (winner == "X" and is_a_x) or (winner == "O" and not is_a_x):
                results["a_wins"] += 1
            else:
                results["b_wins"] += 1

        results["avg_latency_a_ms"] = sum(latencies_a) / max(1, len(latencies_a))
        results["avg_latency_b_ms"] = sum(latencies_b) / max(1, len(latencies_b))
        return results
