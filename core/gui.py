import sys
import math
import time
import random
from typing import Dict, Any, List, Optional, Tuple

import pygame
from core.game import TicTacToeBoard
from core.engines import (
    BaseEngine,
    AlphaBetaEngine,
    MonteCarloTreeSearchEngine,
    RuleBasedHeuristicEngine,
    RandomEngine,
    MoveTelemetry,
    CandidateMoveEval
)
from core.comparison import HeadToHeadBenchmark

# -------------------------------------------------------------------------
# UI Color Palette & Design Tokens
# -------------------------------------------------------------------------
COLOR_BG = (15, 17, 23)
COLOR_PANEL_BG = (22, 27, 34)
COLOR_CARD_BG = (30, 36, 46)
COLOR_CARD_HOVER = (38, 46, 59)
COLOR_BORDER = (48, 54, 61)

COLOR_ACCENT = (0, 212, 255)
COLOR_ACCENT_HOVER = (64, 224, 255)
COLOR_ACCENT_MUTED = (0, 100, 120)

COLOR_X = (255, 75, 75)
COLOR_O = (0, 220, 180)

COLOR_TEXT_PRIMARY = (240, 246, 252)
COLOR_TEXT_SECONDARY = (139, 148, 158)
COLOR_TEXT_MUTED = (110, 118, 129)

COLOR_WIN_GREEN = (46, 160, 67)
COLOR_DRAW_AMBER = (210, 153, 34)
COLOR_LOSS_RED = (248, 81, 73)


# -------------------------------------------------------------------------
# Reusable UI Controls
# -------------------------------------------------------------------------
class Button:
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font,
                 bg_color=COLOR_CARD_BG, hover_color=COLOR_CARD_HOVER, text_color=COLOR_TEXT_PRIMARY):
        self.rect = rect
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface: pygame.Surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, width=1, border_radius=6)

        txt_surf = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)


class Dropdown:
    def __init__(self, rect: pygame.Rect, options: List[str], font: pygame.font.Font, selected_idx: int = 0):
        self.rect = rect
        self.options = options
        self.font = font
        self.selected_idx = selected_idx
        self.is_open = False
        self.hovered_opt = -1

    @property
    def selected_value(self) -> str:
        return self.options[self.selected_idx]

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_open:
                # Check option click
                for i in range(len(self.options)):
                    opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if opt_rect.collidepoint(event.pos):
                        self.selected_idx = i
                        self.is_open = False
                        return True
                self.is_open = False
            else:
                if self.rect.collidepoint(event.pos):
                    self.is_open = True
                    return True
        elif event.type == pygame.MOUSEMOTION and self.is_open:
            self.hovered_opt = -1
            for i in range(len(self.options)):
                opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                if opt_rect.collidepoint(event.pos):
                    self.hovered_opt = i
        return False

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, COLOR_CARD_BG, self.rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, width=1, border_radius=6)

        label = self.font.render(self.selected_value, True, COLOR_TEXT_PRIMARY)
        surface.blit(label, (self.rect.x + 12, self.rect.y + (self.rect.height - label.get_height()) // 2))

        # Arrow icon
        arrow = "▲" if self.is_open else "▼"
        arrow_surf = self.font.render(arrow, True, COLOR_TEXT_MUTED)
        surface.blit(arrow_surf, (self.rect.right - 24, self.rect.y + (self.rect.height - arrow_surf.get_height()) // 2))

    def draw_dropdown_list(self, surface: pygame.Surface):
        if not self.is_open:
            return
        total_h = len(self.options) * self.rect.height
        dropdown_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, total_h)
        pygame.draw.rect(surface, (20, 24, 32), dropdown_rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_ACCENT, dropdown_rect, width=1, border_radius=6)

        for i, opt in enumerate(self.options):
            opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
            if i == self.hovered_opt:
                pygame.draw.rect(surface, COLOR_CARD_HOVER, opt_rect)

            txt = self.font.render(opt, True, COLOR_ACCENT if i == self.selected_idx else COLOR_TEXT_PRIMARY)
            surface.blit(txt, (opt_rect.x + 12, opt_rect.y + (opt_rect.height - txt.get_height()) // 2))


# -------------------------------------------------------------------------
# Main Game-Grade UI Engine
# -------------------------------------------------------------------------
class TicTacToeApp:
    def __init__(self, root=None):
        pygame.init()
        pygame.font.init()

        # Display Setup
        self.screen_w = 1280
        self.screen_h = 760
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.RESIZABLE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Tic-Tac-Toe AI Laboratory — Production Engine")

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True

        # Fonts
        self.font_large = pygame.font.SysFont("Segoe UI, Helvetica, Arial", 32, bold=True)
        self.font_medium = pygame.font.SysFont("Segoe UI, Helvetica, Arial", 18, bold=True)
        self.font_regular = pygame.font.SysFont("Segoe UI, Helvetica, Arial", 14)
        self.font_small = pygame.font.SysFont("Segoe UI, Helvetica, Arial", 12)
        self.font_mono = pygame.font.SysFont("Consolas, Courier New, monospace", 13)

        # Game State
        self.board = TicTacToeBoard()
        self.human_symbol = "X"
        self.ai_symbol = "O"
        self.game_active = True
        self.status_text = "Your Turn (X)"
        self.status_color = COLOR_X
        self.last_telemetry: Optional[MoveTelemetry] = None
        self.hovered_cell: Optional[int] = None
        self.show_heatmaps = True

        # Mode Selection
        self.current_tab = "arena"  # "arena" or "benchmark"
        self.mode_type = "algorithm"  # "algorithm" or "difficulty"

        self.engine_factories = {
            "Alpha-Beta Pruning": lambda sym: AlphaBetaEngine(sym, use_pruning=True),
            "Pure Minimax": lambda sym: AlphaBetaEngine(sym, use_pruning=False),
            "Monte Carlo (MCTS)": lambda sym: MonteCarloTreeSearchEngine(sym, simulations=1500),
            "Rule-Based Expert": lambda sym: RuleBasedHeuristicEngine(sym),
            "Random Baseline": lambda sym: RandomEngine(sym)
        }
        self.difficulty_levels = ["Unbeatable (Master)", "Intermediate (Medium)", "Casual (Easy)"]

        # Tournament State
        self.tournament_running = False
        self.tournament_results: Optional[Dict[str, Any]] = None

        self._init_controls()

    def _init_controls(self):
        # Navigation Buttons
        self.btn_tab_arena = Button(pygame.Rect(20, 15, 180, 36), "Arena & Telemetry", self.font_regular, bg_color=COLOR_ACCENT_MUTED)
        self.btn_tab_bench = Button(pygame.Rect(210, 15, 180, 36), "Engine Tournament", self.font_regular)
        self.btn_fullscreen = Button(pygame.Rect(self.screen_w - 140, 15, 120, 36), "Toggle Full (F11)", self.font_small)

        # Action Buttons
        self.btn_reset = Button(pygame.Rect(0, 0, 120, 34), "Restart", self.font_medium, bg_color=COLOR_ACCENT, text_color=(0, 0, 0))
        self.btn_ai_first = Button(pygame.Rect(0, 0, 120, 34), "AI Move First", self.font_regular)
        self.btn_heatmap = Button(pygame.Rect(0, 0, 120, 34), "Toggle Heatmap", self.font_regular)

        # Dropdowns
        self.dd_engine = Dropdown(pygame.Rect(0, 0, 220, 34), list(self.engine_factories.keys()), self.font_regular, 0)
        self.dd_difficulty = Dropdown(pygame.Rect(0, 0, 220, 34), self.difficulty_levels, self.font_regular, 0)

        # Tournament Controls
        self.dd_tourney_a = Dropdown(pygame.Rect(40, 130, 240, 36), list(self.engine_factories.keys()), self.font_regular, 0)
        self.dd_tourney_b = Dropdown(pygame.Rect(320, 130, 240, 36), list(self.engine_factories.keys()), self.font_regular, 2)
        self.btn_run_tournament = Button(pygame.Rect(590, 130, 200, 36), "Run 50-Game Sim", self.font_medium, bg_color=COLOR_ACCENT, text_color=(0, 0, 0))

    def _get_active_engine(self) -> BaseEngine:
        if self.mode_type == "algorithm":
            name = self.dd_engine.selected_value
            return self.engine_factories[name](self.ai_symbol)
        else:
            diff = self.dd_difficulty.selected_value
            if diff == "Casual (Easy)":
                return RandomEngine(self.ai_symbol) if random.random() < 0.75 else RuleBasedHeuristicEngine(self.ai_symbol)
            elif diff == "Intermediate (Medium)":
                return RuleBasedHeuristicEngine(self.ai_symbol)
            else:
                return AlphaBetaEngine(self.ai_symbol, use_pruning=True)

    def _on_cell_clicked(self, cell_idx: int):
        if not self.game_active:
            return
        if cell_idx in self.board.get_legal_moves():
            self.board = self.board.make_move(cell_idx, self.human_symbol)
            if self._check_game_over():
                return
            self.status_text = "AI Thinking..."
            self.status_color = COLOR_O
            self._render_frame()  # Immediate render update

            # Run AI step
            pygame.time.delay(40)
            self._execute_ai_turn()

    def _execute_ai_turn(self):
        if not self.game_active or self.board.is_terminal():
            return
        engine = self._get_active_engine()
        telemetry = engine.select_move(self.board)
        self.last_telemetry = telemetry
        self.board = self.board.make_move(telemetry.best_move, self.ai_symbol)

        if not self._check_game_over():
            self.status_text = "Your Turn (X)"
            self.status_color = COLOR_X

    def _check_game_over(self) -> bool:
        winner = self.board.check_winner()
        if winner:
            self.game_active = False
            self.status_text = "VICTORY: You Won!" if winner == self.human_symbol else "DEFEAT: AI Engine Wins!"
            self.status_color = COLOR_WIN_GREEN if winner == self.human_symbol else COLOR_LOSS_RED
            return True
        elif self.board.is_full():
            self.game_active = False
            self.status_text = "GAME OVER: Theoretical Draw!"
            self.status_color = COLOR_DRAW_AMBER
            return True
        return False

    def reset_game(self):
        self.board = TicTacToeBoard()
        self.game_active = True
        self.last_telemetry = None
        self.status_text = "Your Turn (X)"
        self.status_color = COLOR_X

    # -------------------------------------------------------------------------
    # Render Loop
    # -------------------------------------------------------------------------
    def _render_frame(self):
        self.screen.fill(COLOR_BG)

        # Top Navigation Bar
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, pygame.Rect(0, 0, self.screen_w, 64))
        pygame.draw.line(self.screen, COLOR_BORDER, (0, 64), (self.screen_w, 64), 1)

        self.btn_tab_arena.bg_color = COLOR_ACCENT_MUTED if self.current_tab == "arena" else COLOR_CARD_BG
        self.btn_tab_bench.bg_color = COLOR_ACCENT_MUTED if self.current_tab == "benchmark" else COLOR_CARD_BG
        self.btn_tab_arena.draw(self.screen)
        self.btn_tab_bench.draw(self.screen)
        self.btn_fullscreen.draw(self.screen)

        if self.current_tab == "arena":
            self._render_arena_view()
        else:
            self._render_tournament_view()

        # Render open dropdowns on top of everything
        if self.current_tab == "arena":
            if self.mode_type == "algorithm":
                self.dd_engine.draw_dropdown_list(self.screen)
            else:
                self.dd_difficulty.draw_dropdown_list(self.screen)
        else:
            self.dd_tourney_a.draw_dropdown_list(self.screen)
            self.dd_tourney_b.draw_dropdown_list(self.screen)

        pygame.display.flip()

    def _render_arena_view(self):
        # Dynamic responsive layout
        left_w = int(self.screen_w * 0.52)
        right_w = self.screen_w - left_w

        # --- Left Board Section ---
        ctrl_y = 80
        # Mode switch tabs
        mode_btn_w = 110
        btn_algo_color = COLOR_ACCENT if self.mode_type == "algorithm" else COLOR_CARD_BG
        btn_diff_color = COLOR_ACCENT if self.mode_type == "difficulty" else COLOR_CARD_BG
        txt_algo_color = (0, 0, 0) if self.mode_type == "algorithm" else COLOR_TEXT_PRIMARY
        txt_diff_color = (0, 0, 0) if self.mode_type == "difficulty" else COLOR_TEXT_PRIMARY

        b1 = Button(pygame.Rect(40, ctrl_y, mode_btn_w, 32), "Engines", self.font_small, bg_color=btn_algo_color, text_color=txt_algo_color)
        b2 = Button(pygame.Rect(160, ctrl_y, mode_btn_w, 32), "Difficulty", self.font_small, bg_color=btn_diff_color, text_color=txt_diff_color)
        b1.draw(self.screen)
        b2.draw(self.screen)

        # Dropdowns & Action Buttons
        drop_x = 290
        if self.mode_type == "algorithm":
            self.dd_engine.rect = pygame.Rect(drop_x, ctrl_y, 220, 32)
            self.dd_engine.draw(self.screen)
        else:
            self.dd_difficulty.rect = pygame.Rect(drop_x, ctrl_y, 220, 32)
            self.dd_difficulty.draw(self.screen)

        # Quick Control row
        btn_row_y = ctrl_y + 44
        self.btn_reset.rect = pygame.Rect(40, btn_row_y, 110, 32)
        self.btn_ai_first.rect = pygame.Rect(160, btn_row_y, 130, 32)
        self.btn_heatmap.rect = pygame.Rect(300, btn_row_y, 130, 32)
        self.btn_reset.draw(self.screen)
        self.btn_ai_first.draw(self.screen)
        self.btn_heatmap.draw(self.screen)

        # Render 3x3 Board
        board_area_y = btn_row_y + 50
        avail_h = self.screen_h - board_area_y - 60
        board_dim = min(left_w - 80, avail_h)
        board_x = 40 + (left_w - 80 - board_dim) // 2
        board_y = board_area_y + (avail_h - board_dim) // 2
        sq_size = board_dim // 3

        # Board Background & Drop Shadow
        pygame.draw.rect(self.screen, (10, 12, 16), (board_x + 6, board_y + 6, board_dim, board_dim), border_radius=12)
        pygame.draw.rect(self.screen, COLOR_CARD_BG, (board_x, board_y, board_dim, board_dim), border_radius=12)
        pygame.draw.rect(self.screen, COLOR_BORDER, (board_x, board_y, board_dim, board_dim), width=2, border_radius=12)

        # Draw Grid Lines
        for i in range(1, 3):
            lx = board_x + i * sq_size
            ly = board_y + i * sq_size
            pygame.draw.line(self.screen, COLOR_BORDER, (lx, board_y + 12), (lx, board_y + board_dim - 12), 3)
            pygame.draw.line(self.screen, COLOR_BORDER, (board_x + 12, ly), (board_x + board_dim - 12, ly), 3)

        # Evaluate candidate heatmaps
        eval_map = {}
        if self.last_telemetry and self.show_heatmaps:
            eval_map = {c.cell_index: c.score for c in self.last_telemetry.candidate_evaluations}

        # Draw Cells & Hover States
        mx, my = pygame.mouse.get_pos()
        self.hovered_cell = None

        for idx in range(9):
            r = idx // 3
            c = idx % 3
            cx = board_x + c * sq_size
            cy = board_y + r * sq_size
            cell_rect = pygame.Rect(cx, cy, sq_size, sq_size)

            val = self.board.state[idx]

            # Hover highlight
            if cell_rect.collidepoint(mx, my) and self.game_active and val is None:
                self.hovered_cell = idx
                hover_surf = pygame.Surface((sq_size - 8, sq_size - 8), pygame.SRCALPHA)
                hover_surf.fill((255, 255, 255, 12))
                self.screen.blit(hover_surf, (cx + 4, cy + 4))

            # Candidate Heatmap Badges
            if val is None and idx in eval_map:
                score = eval_map[idx]
                badge_col = COLOR_WIN_GREEN if score > 0 else (COLOR_DRAW_AMBER if score == 0 else COLOR_LOSS_RED)
                score_str = f"{score:+.1f}"
                badge_surf = self.font_small.render(score_str, True, badge_col)
                self.screen.blit(badge_surf, (cx + sq_size - badge_surf.get_width() - 10, cy + 8))

            # Render Glyphs
            center_x = cx + sq_size // 2
            center_y = cy + sq_size // 2

            if val == "X":
                offset = int(sq_size * 0.28)
                thick = max(6, int(sq_size * 0.08))
                pygame.draw.line(self.screen, COLOR_X, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), thick)
                pygame.draw.line(self.screen, COLOR_X, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), thick)
            elif val == "O":
                rad = int(sq_size * 0.28)
                thick = max(6, int(sq_size * 0.08))
                pygame.draw.circle(self.screen, COLOR_O, (center_x, center_y), rad, thick)

        # Status text below board
        status_surf = self.font_medium.render(self.status_text, True, self.status_color)
        self.screen.blit(status_surf, (board_x, board_y + board_dim + 16))

        # --- Right Telemetry Panel ---
        rx = left_w + 10
        ry = 80
        rw = right_w - 30
        rh = self.screen_h - 100

        panel_rect = pygame.Rect(rx, ry, rw, rh)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_BORDER, panel_rect, width=1, border_radius=12)

        # Title
        t_title = self.font_medium.render("LIVE ENGINE TELEMETRY", True, COLOR_ACCENT)
        self.screen.blit(t_title, (rx + 20, ry + 16))

        # Metrics Grid Card
        card_y = ry + 48
        card_w = rw - 40
        pygame.draw.rect(self.screen, COLOR_CARD_BG, (rx + 20, card_y, card_w, 140), border_radius=8)

        t = self.last_telemetry
        eng_name = t.engine_name if t else "Ready"
        latency_str = f"{t.duration_ms:.2f} ms" if t else "0.00 ms"
        nodes_str = f"{t.nodes_evaluated:,}" if t else "0"
        depth_str = f"{t.max_depth_reached} plies" if t else "0"
        prune_str = f"{t.pruned_branches} subtrees" if t else "0"
        conf_str = f"{t.confidence_score:+.2f}" if t else "0.00"

        metrics = [
            ("Engine Active:", eng_name, COLOR_TEXT_PRIMARY),
            ("Execution Time:", latency_str, COLOR_ACCENT),
            ("Nodes Evaluated:", nodes_str, COLOR_TEXT_PRIMARY),
            ("Max Search Depth:", depth_str, COLOR_TEXT_PRIMARY),
            ("Branches Pruned:", prune_str, COLOR_TEXT_PRIMARY),
            ("Move Confidence:", conf_str, COLOR_WIN_GREEN if (t and t.confidence_score > 0) else COLOR_DRAW_AMBER)
        ]

        for i, (k, v, col) in enumerate(metrics):
            gx = rx + 32 + (i % 2) * (card_w // 2)
            gy = card_y + 12 + (i // 2) * 40
            k_surf = self.font_small.render(k, True, COLOR_TEXT_MUTED)
            v_surf = self.font_small.render(v, True, col)
            self.screen.blit(k_surf, (gx, gy))
            self.screen.blit(v_surf, (gx, gy + 16))

        # Strategic Rationale Section
        sec_y = card_y + 155
        self.screen.blit(self.font_small.render("WHY PLAY THIS MOVE:", True, COLOR_ACCENT), (rx + 20, sec_y))
        reason_box = pygame.Rect(rx + 20, sec_y + 20, card_w, 65)
        pygame.draw.rect(self.screen, COLOR_CARD_BG, reason_box, border_radius=6)

        reason_txt = t.reasoning if t else "Engine waiting for initial human move..."
        self._blit_wrapped_text(reason_txt, rx + 28, sec_y + 28, card_w - 16, self.font_small, COLOR_TEXT_PRIMARY)

        # Alternative Move Rejections
        sec2_y = sec_y + 98
        self.screen.blit(self.font_small.render("SUBOPTIMAL MOVE DISCARD SUMMARY:", True, COLOR_LOSS_RED), (rx + 20, sec2_y))
        discard_box = pygame.Rect(rx + 20, sec2_y + 20, card_w, 55)
        pygame.draw.rect(self.screen, COLOR_CARD_BG, discard_box, border_radius=6)

        disc_txt = t.why_discarded if (t and t.why_discarded) else "No candidate moves discarded yet."
        self._blit_wrapped_text(disc_txt, rx + 28, sec2_y + 26, card_w - 16, self.font_small, COLOR_TEXT_MUTED)

        # Candidate Move Ranking Table
        table_y = sec2_y + 88
        self.screen.blit(self.font_small.render("LEGAL MOVE RANKINGS:", True, COLOR_TEXT_PRIMARY), (rx + 20, table_y))

        headers = ["Sq", "Score", "Nodes/Visits", "Rationale"]
        col_x = [rx + 20, rx + 65, rx + 130, rx + 230]

        th_y = table_y + 20
        for i, h in enumerate(headers):
            self.screen.blit(self.font_small.render(h, True, COLOR_TEXT_MUTED), (col_x[i], th_y))
        pygame.draw.line(self.screen, COLOR_BORDER, (rx + 20, th_y + 18), (rx + 20 + card_w, th_y + 18), 1)

        row_y = th_y + 24
        if t and t.candidate_evaluations:
            for eval_c in t.candidate_evaluations[:6]:
                sq_txt = f"#{eval_c.cell_index}"
                sc_txt = f"{eval_c.score:+.2f}"
                nd_txt = str(eval_c.visits_or_nodes)
                sc_col = COLOR_WIN_GREEN if eval_c.score > 0 else (COLOR_DRAW_AMBER if eval_c.score == 0 else COLOR_LOSS_RED)

                self.screen.blit(self.font_mono.render(sq_txt, True, COLOR_TEXT_PRIMARY), (col_x[0], row_y))
                self.screen.blit(self.font_mono.render(sc_txt, True, sc_col), (col_x[1], row_y))
                self.screen.blit(self.font_mono.render(nd_txt, True, COLOR_TEXT_SECONDARY), (col_x[2], row_y))

                rat_surf = self.font_small.render(eval_c.rationale[:35], True, COLOR_TEXT_MUTED)
                self.screen.blit(rat_surf, (col_x[3], row_y))
                row_y += 24

    def _render_tournament_view(self):
        # Comparison Tab Setup
        self.screen.blit(self.font_large.render("ALGORITHM VS ALGORITHM TOURNAMENT", True, COLOR_TEXT_PRIMARY), (40, 80))

        # Setup Selectors
        self.screen.blit(self.font_small.render("Player A (Engine 1):", True, COLOR_TEXT_MUTED), (40, 110))
        self.dd_tourney_a.draw(self.screen)

        self.screen.blit(self.font_small.render("Player B (Engine 2):", True, COLOR_TEXT_MUTED), (320, 110))
        self.dd_tourney_b.draw(self.screen)

        self.btn_run_tournament.draw(self.screen)

        # Results Matrix Display
        res_y = 200
        card_w = self.screen_w - 80
        card_h = self.screen_h - res_y - 40
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, (40, res_y, card_w, card_h), border_radius=12)
        pygame.draw.rect(self.screen, COLOR_BORDER, (40, res_y, card_w, card_h), width=1, border_radius=12)

        if not self.tournament_results:
            msg = self.font_medium.render("Select two algorithms above and click 'Run 50-Game Sim' to start tournament.", True, COLOR_TEXT_MUTED)
            self.screen.blit(msg, (80, res_y + 40))
            return

        res = self.tournament_results
        self.screen.blit(self.font_medium.render(f"Simulation Outcome ({res['rounds']} Rounds):", True, COLOR_ACCENT), (70, res_y + 30))

        headers = ["Metric", res["name_a"], res["name_b"]]
        col_x = [70, 420, 750]

        row_y = res_y + 80
        for i, h in enumerate(headers):
            self.screen.blit(self.font_medium.render(h, True, COLOR_TEXT_PRIMARY if i == 0 else COLOR_ACCENT), (col_x[i], row_y))
        pygame.draw.line(self.screen, COLOR_BORDER, (70, row_y + 30), (70 + card_w - 60, row_y + 30), 2)

        metrics = [
            ("Total Victories (Wins)", str(res["a_wins"]), str(res["b_wins"])),
            ("Draws Enforced", str(res["draws"]), str(res["draws"])),
            ("Average Move Latency", f"{res['avg_latency_a_ms']:.2f} ms", f"{res['avg_latency_b_ms']:.2f} ms"),
            ("Total Game Tree Nodes Explored", f"{res['total_nodes_a']:,}", f"{res['total_nodes_b']:,}"),
            ("Algorithmic Guarantee", "Complete & Optimal" if "Minimax" in res["name_a"] or "Alpha-Beta" in res["name_a"] else "Stochastic",
                                     "Complete & Optimal" if "Minimax" in res["name_b"] or "Alpha-Beta" in res["name_b"] else "Stochastic")
        ]

        row_y += 50
        for label, val_a, val_b in metrics:
            self.screen.blit(self.font_regular.render(label, True, COLOR_TEXT_MUTED), (col_x[0], row_y))
            self.screen.blit(self.font_medium.render(val_a, True, COLOR_TEXT_PRIMARY), (col_x[1], row_y))
            self.screen.blit(self.font_medium.render(val_b, True, COLOR_TEXT_PRIMARY), (col_x[2], row_y))
            row_y += 40

    def _blit_wrapped_text(self, text: str, x: int, y: int, max_w: int, font: pygame.font.Font, color: Tuple[int, int, int]):
        words = text.split(" ")
        line = ""
        cur_y = y
        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] < max_w:
                line = test_line
            else:
                self.screen.blit(font.render(line, True, color), (x, cur_y))
                line = word + " "
                cur_y += font.get_linesize()
        if line:
            self.screen.blit(font.render(line, True, color), (x, cur_y))

    # -------------------------------------------------------------------------
    # Main Event Loop
    # -------------------------------------------------------------------------
    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                elif event.type == pygame.VIDEORESIZE:
                    if not self.is_fullscreen:
                        self.screen_w = max(1000, event.w)
                        self.screen_h = max(680, event.h)
                        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.RESIZABLE | pygame.DOUBLEBUF)
                        self._init_controls()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.is_fullscreen = not self.is_fullscreen
                        if self.is_fullscreen:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            self.screen_w, self.screen_h = self.screen.get_size()
                        else:
                            self.screen_w, self.screen_h = 1280, 760
                            self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.RESIZABLE | pygame.DOUBLEBUF)
                        self._init_controls()

                # Process UI Button Events
                if self.btn_fullscreen.handle_event(event):
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F11))
                if self.btn_tab_arena.handle_event(event):
                    self.current_tab = "arena"
                if self.btn_tab_bench.handle_event(event):
                    self.current_tab = "benchmark"

                if self.current_tab == "arena":
                    # Handle Dropdowns first so clicks don't bleed into buttons below
                    active_dd = self.dd_engine if self.mode_type == "algorithm" else self.dd_difficulty
                    if active_dd.handle_event(event):
                        continue

                    # Mode Toggles
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if pygame.Rect(40, 80, 110, 32).collidepoint(event.pos):
                            self.mode_type = "algorithm"
                        elif pygame.Rect(160, 80, 110, 32).collidepoint(event.pos):
                            self.mode_type = "difficulty"

                    if self.btn_reset.handle_event(event):
                        self.reset_game()
                    if self.btn_ai_first.handle_event(event):
                        self.reset_game()
                        self.status_text = "AI Thinking..."
                        self.status_color = COLOR_O
                        self._render_frame()
                        pygame.time.delay(50)
                        self._execute_ai_turn()
                    if self.btn_heatmap.handle_event(event):
                        self.show_heatmaps = not self.show_heatmaps

                    # Click on Board
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.hovered_cell is not None:
                            self._on_cell_clicked(self.hovered_cell)

                elif self.current_tab == "benchmark":
                    if self.dd_tourney_a.handle_event(event):
                        continue
                    if self.dd_tourney_b.handle_event(event):
                        continue

                    if self.btn_run_tournament.handle_event(event):
                        name_a = self.dd_tourney_a.selected_value
                        name_b = self.dd_tourney_b.selected_value
                        fac_a = self.engine_factories[name_a]
                        fac_b = self.engine_factories[name_b]

                        # Show thinking message
                        self.tournament_results = None
                        self._render_frame()
                        self.tournament_results = HeadToHeadBenchmark.run_matchup(fac_a, fac_b, name_a, name_b, rounds=50)

            self._render_frame()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()
