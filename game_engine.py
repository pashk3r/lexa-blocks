import pygame
from constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from event_handler import EventHandler
from game_state import GameState
from renderer import Renderer


class Game:

    def __init__(self, plugin=None):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.renderer = Renderer(self.screen)
        self.event_handler = EventHandler()
        self.plugin = plugin
        self._rects: list[pygame.Rect] = []

    def run(self):
        prev_game_over = False

        while True:
            events = pygame.event.get()
            self.event_handler.process(
                events,
                self.state,
                self._rects,
                plugin=self.plugin
            )

            if self.state.game_over and not prev_game_over:
                if self.plugin:
                    self.plugin.on_game_over(self.state, self.renderer)

            prev_game_over = self.state.game_over

            self._rects = self.renderer.draw_frame(self.state, plugin=self.plugin)
            self.clock.tick(FPS)
