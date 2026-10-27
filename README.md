# ⭕❌ Tic-Tac-Toe AI Laboratory

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Profile](https://img.shields.io/badge/Author-Omar%20Soudan-181717?logo=github)](https://github.com/OmarSoudan)

A game-grade **Game Theory and Artificial Intelligence laboratory** powered by hardware-accelerated Pygame graphics. Pit human intuition against classical and stochastic search paradigms, inspect live counterfactual move heatmaps with millisecond engine dossiers, and execute automated multi-engine tournament simulations.

---

## ⚡ Core Highlights

- **Hardware-Accelerated Pygame GUI**: Smooth 60 FPS vector rendering, glow highlights, dynamic hover states, responsive resizing, and windowless fullscreen (`F11`).
- **Real-Time Candidate Move Heatmap**: Visual evaluation badges overlaying unplayed cells (+1.0 forced victory, 0.0 equilibrium draw, -1.0 concession).
- **Move Decision & Search Dossier**: Live computational telemetry updating on every move:
  - Wall-clock search latency (ms)
  - Evaluated state-space nodes
  - Maximum ply depth reached
  - Alpha-Beta pruned subtrees
  - Natural-language reasoning stream explaining why the chosen move was played and why alternative cells were rejected
- **Engine vs. Engine Tournament Mode**: Run automated $N$-round head-to-head simulations (e.g., Alpha-Beta vs. MCTS) with alternating starting turns to compare win/draw rates, latency curves, and tree efficiency.
- **Dual Match Modes**: Select exact search engines or challenge tiered difficulties (*Casual*, *Intermediate*, *Unbeatable*).

---

## 🔬 Algorithmic Breakdown

| Engine | Search Paradigm | Game-Theoretic Optimality | Search Tree Pruning | Typical Move Latency |
| :--- | :--- | :--- | :--- | :--- |
| **Alpha-Beta Pruning** | Minimax + Cutoff Branches | **Guaranteed Optimal** | $\beta \le \alpha$ subtree pruning | < 4 ms |
| **Pure Minimax** | Exhaustive Backward Induction | **Guaranteed Optimal** | None (Exhaustive leaf evaluation) | ~80–120 ms |
| **MCTS (UCB1)** | Stochastic Rollout Playouts | Asymptotically Optimal | Upper Confidence Bounds selection | ~20–35 ms |
| **Rule-Based Expert** | Priority-Weighted Heuristics | Near-Optimal | Handcrafted tactical hierarchy | < 0.1 ms |
| **Random Baseline** | Uniform Sampling | Stochastic / Naive | None | < 0.01 ms |

---

## 📁 Repository Structure

```text
tic-tac-toe-ai-lab/
├── LICENSE
├── README.md
├── requirements.txt
├── main.py
└── core/
    ├── __init__.py
    ├── game.py              # State representation, terminal checks, win bitmasks
    ├── comparison.py        # Head-to-head tournament benchmark runner
    ├── gui.py               # 60 FPS Pygame graphics engine & telemetry UI
    └── engines/
        ├── __init__.py      # Engine and telemetry exports
        ├── base.py          # Abstract engine interface & candidate evaluation types
        ├── minimax.py       # Alpha-Beta & pure Minimax with alternate move scoring
        ├── mcts.py          # Monte Carlo Tree Search with UCB1 exploration
        ├── heuristic.py     # Priority-matrix rule engine
        └── random_agent.py  # Uniform random sampler


🚀 Getting Started
Prerequisites
Python 3.8 or higher

pip package manager


git clone [https://github.com/OmarSoudan/tic-tac-toe-ai-lab.git](https://github.com/OmarSoudan/tic-tac-toe-ai-lab.git)
cd tic-tac-toe-ai-lab
pip install -r requirements.txt

Launch Interactive Desktop GUI

python main.py

Press F11 to toggle edge-to-edge fullscreen.

Click Toggle Heatmap to display cell-by-cell score evaluations.

Switch to the Engine Tournament tab to run automated matchups.

Run Headless Terminal Profiler
python main.py --benchmark

👨‍💻 Author
Omar Soudan

GitHub: @OmarSoudan

📜 License
Distributed under the MIT License. See LICENSE for details.

