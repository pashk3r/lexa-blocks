class BasePlugin:
    def on_game_over(self, state, renderer) -> bool:
        return False

    def on_restart(self, state):
        pass

    def draw_overlay(self, screen, state, renderer) -> list:
        return []

    def handle_click(self, pos, state, rects) -> bool:
        return False
