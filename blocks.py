import pygame
from constants import CELL_SIZE


class Block:

    def __init__(self, shape, color, slot_pos):
        self.shape = shape
        self.color = color
        self.original_slot_pos = pygame.Vector2(slot_pos)
        self.pos = pygame.Vector2(slot_pos)
        self.is_placed = False

    def draw(self, surface, scale=1.0):
        if self.is_placed:
            return

        for dx, dy in self.shape:
            rect = pygame.Rect(
                self.pos.x + dx * CELL_SIZE * scale,
                self.pos.y + dy * CELL_SIZE * scale,
                CELL_SIZE * scale - 2,
                CELL_SIZE * scale - 2
            )
            pygame.draw.rect(surface, self.color, rect, border_radius=5)

    def collide_point(self, point):
        for dx, dy in self.shape:
            rect = pygame.Rect(
                self.pos.x + dx * CELL_SIZE,
                self.pos.y + dy * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            if rect.collidepoint(point):
                return True
        return False
