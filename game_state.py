import random
import pygame

from blocks import Block
from board import Board
from constants import (
    GRID_SIZE, MARGIN, CELL_SIZE,
    SHAPES, COLORS,
    SLOT_X_START, SLOT_SPACING, SLOT_Y,
    STATE_GAME_OVER
)


class GameState:

    def __init__(self):
        self.board = Board()
        self.blocks_in_hand: list[Block] = []
        self.active_block: Block | None = None
        self.drag_offset = pygame.Vector2(0, 0)
        self.score = 0
        self.level = 1
        self.game_over = False
        self.go_state = STATE_GAME_OVER
        self.question_text = ""
        self.options: list[str] = []
        self.correct_index = 0
        self.selected_index: int | None = None
        self.spawn_blocks()

    def spawn_blocks(self):
        self.blocks_in_hand = [
            Block(
                random.choice(SHAPES),
                random.choice(COLORS["blocks"]),
                (SLOT_X_START + i * SLOT_SPACING, SLOT_Y)
            )
            for i in range(3)
        ]

    def spawn_rescue_blocks(self):
        self.blocks_in_hand = [
            Block(
                [(0, 0)],
                random.choice(COLORS["blocks"]),
                (SLOT_X_START + i * SLOT_SPACING, SLOT_Y)
            )
            for i in range(3)
        ]

    def try_place_active_block(self) -> bool:
        if self.active_block is None:
            return False

        gx = round((self.active_block.pos.x - MARGIN) / CELL_SIZE)
        gy = round((self.active_block.pos.y - MARGIN) / CELL_SIZE)

        if self.board.can_place(self.active_block, gx, gy):
            points = self.board.place(self.active_block, gx, gy)
            self._add_score(points)
            self.blocks_in_hand.remove(self.active_block)
            self.active_block = None

            if not self.blocks_in_hand:
                self.spawn_blocks()

            if self._is_game_over():
                self.game_over = True

            return True

        self.active_block.pos = self.active_block.original_slot_pos
        self.active_block = None
        return False

    def pick_block(self, point):
        for block in self.blocks_in_hand:
            if block.collide_point(point):
                self.active_block = block
                self.drag_offset = pygame.Vector2(block.pos) - pygame.Vector2(point)
                return

    def drag_active_block(self, point):
        if self.active_block:
            self.active_block.pos = pygame.Vector2(point) + self.drag_offset

    def _add_score(self, points):
        self.score += points
        self.level = self.score // 100 + 1

    def _is_game_over(self) -> bool:
        return not any(
            self.board.can_place(block, gx, gy)
            for block in self.blocks_in_hand
            for gy in range(GRID_SIZE)
            for gx in range(GRID_SIZE)
        )

    def apply_question(self, question_text: str, options: list[str], correct_index: int):
        self.question_text = question_text
        self.options = options
        self.correct_index = correct_index

    def clear_question(self):
        self.question_text = ""
        self.options = []
        self.correct_index = 0
        self.selected_index = None