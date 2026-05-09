import pygame
from constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from event_handler import EventHandler
from game_state import GameState
from renderer import Renderer


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.renderer = Renderer(self.screen)
        self.event_handler = EventHandler()
        self._rects: list = []

    def run(self):
        while True:
            events = pygame.event.get()
            self.event_handler.process(events, self.state, self._rects)
            self._rects = self.renderer.draw_frame(self.state)
            self.clock.tick(FPS)
