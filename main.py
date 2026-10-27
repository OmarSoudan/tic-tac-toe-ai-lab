import argparse
from core.gui import TicTacToeApp
from core.game import TicTacToeBoard
from core.engines import (
    AlphaBetaEngine,
    MonteCarloTreeSearchEngine,
    RuleBasedHeuristicEngine,
    RandomEngine
)

def benchmark():
    """Runs a programmatic speed and decision benchmark across all engines."""
    engines = [
        AlphaBetaEngine("O", use_pruning=True),
        AlphaBetaEngine("O", use_pruning=False),
        MonteCarloTreeSearchEngine("O", simulations=1000),
        RuleBasedHeuristicEngine("O"),
        RandomEngine("O")
    ]

    # Test position: center occupied, human on corner (1 turn in)
    test_board = TicTacToeBoard((
        "X", None, None,
        None, "O", None,
        None, None, None
    ))

    print("\n" + "=" * 65)
    print("      TIC-TAC-TOE ENGINE COMPUTATIONAL BENCHMARK")
    print("=" * 65)
    print(f"{'Engine':<28} | {'Move':<5} | {'Latency':<9} | {'Nodes':<8} | {'Depth'}")
    print("-" * 65)

    for eng in engines:
        t = eng.select_move(test_board)
        name = t.engine_name[:26]
        print(f"{name:<28} | {t.best_move:<5} | {t.duration_ms:6.2f} ms | {t.nodes_evaluated:<8} | {t.max_depth_reached} plies")
    print("=" * 65 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Tic-Tac-Toe AI Laboratory")
    parser.add_argument("--benchmark", action="store_true", help="Run headless engine speed benchmark")
    args = parser.parse_args()

    if args.benchmark:
        benchmark()
    else:
        app = TicTacToeApp()
        app.mainloop()

if __name__ == "__main__":
    main()
