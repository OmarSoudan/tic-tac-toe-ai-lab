from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from core.game import TicTacToeBoard

@dataclass
class CandidateMoveEval:
    cell_index: int
    score: float             # Normalized [-1.0 (loss), 0.0 (draw), +1.0 (win)]
    visits_or_nodes: int = 0
    rationale: str = ""

@dataclass
class MoveTelemetry:
    best_move: int
    candidate_evaluations: List[CandidateMoveEval] = field(default_factory=list)
    nodes_evaluated: int = 0
    max_depth_reached: int = 0
    pruned_branches: int = 0
    duration_ms: float = 0.0
    confidence_score: float = 0.0
    engine_name: str = ""
    reasoning: str = ""
    why_discarded: str = ""
    extra_stats: Dict[str, Any] = field(default_factory=dict)

class BaseEngine(ABC):
    def __init__(self, player_symbol: str = "O"):
        self.symbol = player_symbol
        self.opponent_symbol = "X" if player_symbol == "O" else "O"

    @abstractmethod
    def select_move(self, board: TicTacToeBoard) -> MoveTelemetry:
        pass
