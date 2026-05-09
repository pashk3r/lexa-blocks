import pygame
from constants import STATE_GAME_OVER


class EventHandler:

    def process(self, events, state, option_rects: list, plugin=None):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if state.game_over:
                self._handle_overlay(event, state, option_rects, plugin)
            else:
                self._handle_game(event, state)

    def _handle_game(self, event, state):
        if event.type == pygame.MOUSEBUTTONDOWN:
            state.pick_block(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if state.active_block:
                state.try_place_active_block()
        elif event.type == pygame.MOUSEMOTION:
            state.drag_active_block(event.pos)

    def _handle_overlay(self, event, state, rects, plugin):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if plugin and state.go_state != STATE_GAME_OVER:
            handled = plugin.handle_click(event.pos, state, rects)
            if handled:
                return

        if state.go_state == STATE_GAME_OVER and rects:
            restart_btn = rects[0]
            if restart_btn.collidepoint(event.pos):
                state.__init__()
                if plugin:
                    plugin.on_restart(state)
