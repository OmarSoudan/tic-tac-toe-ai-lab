# ⭕❌ Tic-Tac-Toe AI Laboratory

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License" />
  <img src="https://img.shields.io/badge/author-Omar%20Soudan-181717?logo=github" alt="Author Omar Soudan" />
</p>

A polished, game-grade Tic-Tac-Toe research environment for exploring adversarial search, decision-making, and AI performance in a visually interactive interface. This project combines a modern Pygame UI with several classic and stochastic algorithms to compare strategy quality, speed, and search behavior in real time.

## Overview

This project is designed for experimentation and visualization rather than just gameplay. It lets you:

- play against multiple AI strategies,
- compare minimax-style search with stochastic rollout methods,
- inspect live move telemetry and reasoning,
- run head-to-head engine simulations,
- benchmark algorithmic performance under different board states.

The application is built around a clean game engine and modular AI architecture, making it easy to extend with additional agents or evaluation metrics.

---

## Features

- Hardware-accelerated Pygame interface with responsive layout and fullscreen support
- Real-time candidate evaluation heatmap for legal moves
- Live telemetry for each move including:
  - search latency,
  - node counts,
  - max depth reached,
  - pruning statistics,
  - strategic rationale
- Engine-vs-engine tournament mode with alternating starting turns
- Dual play modes:
  - exact algorithm selection,
  - difficulty-based challenges
- Benchmark runner for comparing search quality and computational cost

---

## Available Engines

| Engine | Search Paradigm | Typical Behavior | Tradeoff |
| :--- | :--- | :--- | :--- |
| Alpha-Beta Pruning | Minimax + pruning | Strong and efficient | Excellent decision quality with low latency |
| Pure Minimax | Exhaustive game-tree search | Optimal but computationally heavier | Slower on larger search horizons |
| MCTS (UCB1) | Monte Carlo rollouts | Approximates strong play via stochastic simulation | Good for uncertainty and faster exploratory evaluation |
| Rule-Based Expert | Heuristic tactical rules | Fast and human-like | Not guaranteed optimal |
| Random Baseline | Uniform random play | Unstructured decisions | Useful as a baseline comparator |

---

## Repository Structure

```text
 tic-tac-toe-ai-lab/
├── LICENSE
├── README.md
├── requirements.txt
├── main.py
└── core/
    ├── __init__.py
    ├── game.py               # Core game logic, board state, win detection
    ├── comparison.py         # Tournament benchmark runner
    ├── gui.py                # Pygame UI and experimental controls
    └── engines/
        ├── __init__.py      # Exports all engine implementations
        ├── base.py          # Abstract engine interface and telemetry models
        ├── minimax.py       # Alpha-Beta and pure minimax implementations
        ├── mcts.py          # Monte Carlo Tree Search with UCB1
        ├── heuristic.py     # Rule-based tactical AI
        └── random_agent.py  # Random move generator
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

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

### Optional: run the headless benchmark

```bash
python main.py --benchmark
```

This prints a quick table comparing engine latency, search depth, and node counts for a representative board state.

---

## How to Use the Application

1. Launch the GUI with `python main.py`.
2. Select an engine or difficulty mode.
3. Play against the AI or let two engines compete.
4. Toggle the heatmap to inspect move-quality estimates.
5. Press `F11` to toggle fullscreen.
6. Open the tournament tab to run a multi-game comparison between algorithms.

### Controls

- `F11`: toggle fullscreen
- Restart: reset the board
- AI Move First: let the computer start
- Toggle Heatmap: show or hide evaluated move scores

---

## Technologies

- Python 3.8+
- Pygame for visualization and interaction
- NumPy for numerical and evaluation-related processing
- Search and decision algorithms for game-playing intelligence

---

## Benchmarking Notes

The project includes a lightweight benchmark runner used to assess computational characteristics of each strategy. This is useful for comparing:

- average search time per move,
- number of nodes evaluated,
- maximum search depth,
- overall quality of generated decisions in a controlled test position.

---

## Project Goals

This laboratory is designed to make AI search methods tangible and understandable:

- visualize board evaluation,
- compare exact and approximate decision-making,
- study pruning behavior,
- demonstrate how heuristics and stochastic search differ from minimax-based optimal play.

---
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/88149289-ceec-4f70-9ae2-5cc43f4e1a57" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a85fed68-5826-4395-9742-0e9ada8dc67c" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5ed48290-fc33-45a3-b290-e4c07c16d303" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3abf3e5a-1fa5-4d49-a683-074f18524139" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9bbafe44-98b5-4759-ab45-64e3513b02fa" />




## Author

Omar Soudan

GitHub: [@OmarSoudan](https://github.com/OmarSoudan)


---

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Issues, feature ideas, and pull requests are welcome. This project is well-suited for experimentation with additional engines, improved heuristics, and richer analytics dashboards.
