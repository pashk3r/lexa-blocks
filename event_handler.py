import pygame


class EventHandler:

    def process(self, events, state, restart_rects: list):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if state.game_over:
                self._handle_game_over(event, state, restart_rects)
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

    def _handle_game_over(self, event, state, rects):
        if event.type == pygame.MOUSEBUTTONDOWN and rects:
            if rects[0].collidepoint(event.pos):
                state.__init__()
