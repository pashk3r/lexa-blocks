import pygame

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MARGIN,
    COLORS
)


class Renderer:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_big = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_med = pygame.font.SysFont("Arial", 24)
        self.font_small = pygame.font.SysFont("Arial", 20, bold=True)

    def draw_frame(self, state) -> list:
        self.screen.fill(COLORS["bg"])
        state.board.draw(self.screen)
        self._draw_score_bar(state)

        for block in state.blocks_in_hand:
            scale = 1.0 if block == state.active_block else 0.8
            block.draw(self.screen, scale)

        rects = []
        if state.game_over:
            rects = self._draw_game_over(state)

        pygame.display.flip()
        return rects

    def _draw_score_bar(self, state):
        bar_x = MARGIN
        bar_y = SCREEN_HEIGHT - 300
        bar_w = SCREEN_WIDTH - MARGIN * 2
        bar_h = 18
        progress = (state.score % 100) / 100

        pygame.draw.rect(
            self.screen, (50, 50, 65),
            (bar_x, bar_y, bar_w, bar_h), border_radius=9
        )
        pygame.draw.rect(
            self.screen, (255, 200, 50),
            (bar_x, bar_y, int(bar_w * progress), bar_h), border_radius=9
        )
        self.screen.blit(
            self.font_small.render(f"Ур. {state.level}", True, (200, 200, 200)),
            (bar_x, bar_y - 24)
        )
        score_surf = self.font_small.render(
            f"{state.score} очков", True, (200, 200, 200)
        )
        self.screen.blit(
            score_surf,
            (bar_x + bar_w - score_surf.get_width(), bar_y - 24)
        )

    def _draw_game_over(self, state) -> list:
        cx = SCREEN_WIDTH // 2

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        self._draw_centered(self.font_big, "Игра окончена!", (255, 80, 80), 260)
        score_text = f"Счёт: {state.score}"
        self._draw_centered(self.font_med, score_text, (200, 200, 200), 320)

        restart_btn = pygame.Rect(0, 0, 200, 50)
        restart_btn.center = (cx, 400)
        pygame.draw.rect(self.screen, (80, 200, 120), restart_btn, border_radius=10)
        self._draw_centered(self.font_med, "Начать заново", (20, 20, 25), 400)

        return [restart_btn]

    def _draw_centered(self, font, text, color, y):
        surf = font.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2, y)))
