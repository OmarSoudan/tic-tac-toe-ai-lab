from typing import List, Optional, Tuple

class TicTacToeBoard:
    """
    Immutable-friendly 3x3 Tic-Tac-Toe board state.
    Represented as a 9-element tuple where empty cells are None,
    and occupied cells are 'X' or 'O'.
    """
    WIN_COMBINATIONS = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    )

    def __init__(self, state: Optional[Tuple[Optional[str], ...]] = None):
        self.state: Tuple[Optional[str], ...] = state if state is not None else tuple([None] * 9)

    def get_legal_moves(self) -> List[int]:
        return [i for i, cell in enumerate(self.state) if cell is None]

    def make_move(self, index: int, player: str) -> "TicTacToeBoard":
        if self.state[index] is not None:
            raise ValueError(f"Cell {index} is already occupied.")
        new_state = list(self.state)
        new_state[index] = player
        return TicTacToeBoard(tuple(new_state))

    def check_winner(self) -> Optional[str]:
        for a, b, c in self.WIN_COMBINATIONS:
            if self.state[a] and (self.state[a] == self.state[b] == self.state[c]):
                return self.state[a]
        return None

    def is_full(self) -> bool:
        return all(cell is not None for cell in self.state)

    def is_terminal(self) -> bool:
        return self.check_winner() is not None or self.is_full()

    def get_result(self, perspective: str) -> Optional[float]:
        winner = self.check_winner()
        if winner == perspective:
            return 1.0
        elif winner is not None:
            return -1.0
        elif self.is_full():
            return 0.0
        return None