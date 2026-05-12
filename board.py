import pygame
from constants import GRID_SIZE, CELL_SIZE, MARGIN, COLORS


class Board:

    def __init__(self):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def draw(self, surface):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                rect = pygame.Rect(
                    MARGIN + c * CELL_SIZE,
                    MARGIN + r * CELL_SIZE,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                )
                color = self.grid[r][c] if self.grid[r][c] else COLORS["grid"]
                pygame.draw.rect(surface, color, rect, border_radius=3)

    def can_place(self, block, gx, gy):
        for dx, dy in block.shape:
            nx, ny = gx + dx, gy + dy
            if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
                return False
            if self.grid[ny][nx]:
                return False
        return True

    def place(self, block, gx, gy):
        for dx, dy in block.shape:
            self.grid[gy + dy][gx + dx] = block.color
        placed_points = len(block.shape)
        line_points = self._clear_lines()
        return placed_points + line_points

    def _find_full_lines(self):
        full_rows = [r for r in range(GRID_SIZE) if all(self.grid[r])]
        full_cols = [
            c for c in range(GRID_SIZE)
            if all(self.grid[r][c] for r in range(GRID_SIZE))
        ]
        return full_rows, full_cols

    def _erase_lines(self, rows, cols):
        for r in rows:
            for c in range(GRID_SIZE):
                self.grid[r][c] = None
        for c in cols:
            for r in range(GRID_SIZE):
                self.grid[r][c] = None

    def _clear_lines(self):
        rows, cols = self._find_full_lines()
        self._erase_lines(rows, cols)
        lines = len(rows) + len(cols)
        return lines * 10 * max(1, lines - 1)