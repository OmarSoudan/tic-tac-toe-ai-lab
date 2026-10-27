# ⭕❌ Tic-Tac-Toe AI & Search Heuristics Laboratory

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Profile](https://img.shields.io/badge/Author-Omar%20Soudan-181717?logo=github)](https://github.com/OmarSoudan)

A multi-paradigm Game Theory and Search benchmark laboratory featuring an interactive desktop GUI. Play against classical minimax variations, Monte Carlo simulations, and heuristic expert agents with real-time computational telemetry (latency, node counts, depth, and pruning metrics) for every move.

---

## ⚡ Core Highlights

- **Dual Interaction Modes**:
  - **Engine Mode**: Play directly against specific search algorithms (Alpha-Beta Pruning, Pure Minimax, MCTS, Expert Rules, Random).
  - **Difficulty Mode**: Battle tiered intelligence levels: *Casual (Easy)*, *Intermediate (Medium)*, and *Unbeatable (Master)*.
- **Move-by-Move Telemetry Dashboard**:
  - Millisecond execution latency
  - Total state space nodes explored
  - Maximum ply depth reached
  - Alpha-Beta pruned subtrees counter
  - Game-theoretic value / confidence score
  - Natural-language engine reasoning stream
- **Zero-Dependency GUI**: Standalone, modern dark-mode interface built on native Python `tkinter`.

---

## 🔬 Algorithmic Comparison

| Engine | Paradigm | Optimality | Avg. Nodes (Ply 1) | Average Latency |
| :--- | :--- | :--- | :--- | :--- |
| **Alpha-Beta Pruning** | Game Tree Search + Branch Cutoff | Guaranteed Optimal | ~2,100 nodes | < 8 ms |
| **Pure Minimax** | Exhaustive Backward Induction | Guaranteed Optimal | ~59,705 nodes | ~120 ms |
| **MCTS (UCB1)** | Stochastic Tree Search & Rollouts | Asymptotically Optimal | Configurable (1,500) | ~25 ms |
| **Rule-Based Expert** | Handcrafted Priority Matrix | Near-Optimal | ~5–9 checks | < 0.1 ms |
| **Random Baseline** | Uniform Sampling | Stochastic / Naive | 1 check | < 0.01 ms |

---

## 🚀 Getting Started

### Installation
```bash
git clone [https://github.com/OmarSoudan/tic-tac-toe-ai-lab.git](https://github.com/OmarSoudan/tic-tac-toe-ai-lab.git)
cd tic-tac-toe-ai-lab
pip install -r requirements.txt