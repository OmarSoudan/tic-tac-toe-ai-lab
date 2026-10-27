# ⭕❌ Tic-Tac-Toe AI Laboratory

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/Pygame-2.x-ffb347?logo=pygame" alt="Pygame" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License" />
  <img src="https://img.shields.io/badge/author-Omar%20Soudan-181717?logo=github" alt="Author Omar Soudan" />
</p>

A polished Tic-Tac-Toe research environment for exploring adversarial search, decision-making, and AI performance in an interactive interface. This project is designed to make classic game AI tangible: you can play against different strategies, inspect move evaluation, compare search algorithms, and run head-to-head simulations without leaving the app.

Whether you're interested in minimax, pruning, stochastic search, or heuristic decision-making, this lab gives you a clean way to compare them side by side.

## Why this project exists

This repository is not just a game. It is a compact AI experimentation platform for studying:

- minimax and alpha-beta pruning,
- Monte Carlo Tree Search (MCTS),
- heuristic rule-based play,
- search efficiency and latency,
- move quality and tactical reasoning,
- performance tradeoffs between exact and approximate strategies.

The goal is to make search behavior visible, interpretable, and easy to compare with a modern, game-like interface.

---

## Features

- Interactive Pygame GUI with responsive controls
- Fullscreen toggle using `F11`
- Multiple AI engines with different strategies
- Real-time move evaluation heatmap
- Live telemetry for each move, including:
  - search latency,
  - node counts,
  - maximum search depth,
  - pruning statistics,
  - strategic rationale
- Engine-vs-engine tournament mode
- Difficulty-based and explicit engine selection modes
- Simple benchmark runner to compare algorithmic cost and quality
- Modular architecture for adding new agents and evaluation metrics

---

## Available engines

| Engine | Search paradigm | Typical behavior | Tradeoff |
| :--- | :--- | :--- | :--- |
| Alpha-Beta Pruning | Minimax + pruning | Strong and efficient | Excellent decision quality with low latency |
| Pure Minimax | Exhaustive game-tree search | Optimal but computationally heavier | Slower on deeper horizons |
| MCTS (UCB1) | Monte Carlo rollouts | Approximate, exploratory play | Good for uncertainty and simulation-heavy decisions |
| Rule-Based Expert | Heuristic tactical rules | Fast and human-like | Not guaranteed optimal |
| Random Baseline | Uniform random play | Unstructured decisions | Useful as a comparison baseline |

---

## Quick start

### Prerequisites

- Python 3.8+
- `pip`
- A terminal or command prompt

### Install

```bash
git clone https://github.com/OmarSoudan/tic-tac-toe-ai-lab.git
cd tic-tac-toe-ai-lab
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the interactive game

```bash
python main.py
```

### Run the benchmark

```bash
python main.py --benchmark
```

This prints a compact comparison of engine latency, search depth, and node counts for a representative board state.

---

## How to use the app

1. Launch the game with `python main.py`.
2. Select an engine or difficulty mode.
3. Play against the AI or let two engines compete.
4. Toggle the heatmap to inspect estimated move quality.
5. Use fullscreen mode with `F11`.
6. Open the tournament panel for head-to-head comparisons between algorithms.

### Controls

- `F11`: toggle fullscreen
- Restart: reset the board
- AI Move First: allow the computer to lead the opening
- Toggle Heatmap: display or hide evaluated move scores

---

## Project structure

```text
tic-tac-toe-ai-lab/
├── LICENSE
├── README.md
├── requirements.txt
├── main.py
└── core/
    ├── __init__.py
    ├── game.py               # Core board logic, move validation, win detection
    ├── comparison.py         # Tournament and benchmark runner
    ├── gui.py                # Pygame UI and experimental controls
    └── engines/
        ├── __init__.py      # Engine exports
        ├── base.py          # Engine interface and telemetry models
        ├── minimax.py       # Alpha-beta and pure minimax implementations
        ├── mcts.py          # Monte Carlo Tree Search with UCB1
        ├── heuristic.py     # Rule-based tactical engine
        └── random_agent.py  # Random move generator
```

---

## Architecture overview

The app is organized around a small but extensible architecture:

- `core/game.py` contains the board state, legal move generation, turn logic, and win checks.
- `core/engines/` defines each strategy as an engine with a common interface.
- `core/gui.py` renders the state and exposes controls for play, benchmarking, and experimentation.
- `core/comparison.py` runs side-by-side comparisons and summary metrics.

This separation keeps the game logic independent from the decision logic, making it easy to add new engines or benchmark scenarios.

---

## Benchmarking notes

The benchmark runner is useful for comparing:

- average search time per move,
- number of nodes explored,
- maximum search depth reached,
- quality of decisions in controlled board states,
- computational cost of each strategy.

This is especially helpful when comparing exact methods (e.g., minimax) with approximate ones (e.g., MCTS or heuristic play).

---

## Research goals

This laboratory is designed to make AI search methods tangible and understandable:

- visualize board evaluation,
- compare exact and approximate decision-making,
- study pruning behavior,
- expose the cost of deeper search,
- demonstrate how heuristic and stochastic strategies differ from optimal minimax play.

---

## Extending the project

The codebase is intentionally modular. You can add new agents by creating a new implementation under `core/engines/` and exposing it through the engine registry or selection system.

Potential extensions include:

- stronger heuristic tactics,
- iterative deepening with time controls,
- transposition tables,
- advanced evaluation functions,
- league-style engine matching,
- statistics dashboards for move correctness and efficiency.

---

## Screenshots

<p align="center">
  <img width="1920" height="1080" alt="Tic-Tac-Toe AI interface" src="https://github.com/user-attachments/assets/88149289-ceec-4f70-9ae2-5cc43f4e1a57" />
</p>

<p align="center">
  <img width="1920" height="1080" alt="Game board and telemetry" src="https://github.com/user-attachments/assets/a85fed68-5826-4395-9742-0e9ada8dc67c" />
  <img width="1920" height="1080" alt="Board evaluation interface" src="https://github.com/user-attachments/assets/5ed48290-fc33-45a3-b290-e4c07c16d303" />
  <img width="1920" height="1080" alt="AI performance view" src="https://github.com/user-attachments/assets/3abf3e5a-1fa5-4d49-a683-074f18524139" />
  <img width="1920" height="1080" alt="Tournament or comparison screen" src="https://github.com/user-attachments/assets/9bbafe44-98b5-4759-ab45-64e3513b02fa" />
</p>

---

## Troubleshooting

### Dependencies fail to install

Make sure you are using Python 3.8 or newer and that your virtual environment is active before running `pip install -r requirements.txt`.

### Pygame window does not appear

Confirm that your display environment supports graphical windows. If you're in a headless environment, the GUI may not launch correctly.

### Benchmark command not behaving as expected

Run the app from the repository root so relative imports resolve correctly.

---

## Author

Omar Soudan

GitHub: [@OmarSoudan](https://github.com/OmarSoudan)

---

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Issues, feature ideas, and pull requests are welcome. This project is well suited for experimentation with additional engines, improved heuristics, richer analytics, and more advanced game AI research.

---

## Summary

This repository blends game design, AI experimentation, and applied computer science in a compact and approachable project. It is a strong example of how classic algorithms can be made interactive, visual, and educational.
