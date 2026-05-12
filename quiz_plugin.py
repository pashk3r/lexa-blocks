import pygame

import api_client
from base_plugin import BasePlugin
from constants import (
    SCREEN_WIDTH,
    STATE_GAME_OVER, STATE_CHOICE, STATE_LOADING,
    STATE_QUESTION, STATE_RESULT_OK, STATE_RESULT_FAIL
)


class QuizPlugin(BasePlugin):

    def on_game_over(self, state, renderer) -> bool:
        state.go_state = STATE_CHOICE
        return True

    def on_restart(self, state):
        state.go_state = STATE_GAME_OVER

    def draw_overlay(self, screen, state, renderer) -> list[pygame.Rect]:
        draw_map = {
            STATE_CHOICE: self._draw_choice,
            STATE_LOADING: self._draw_loading,
            STATE_QUESTION: self._draw_question,
            STATE_RESULT_OK: self._draw_result_ok,
            STATE_RESULT_FAIL: self._draw_result_fail,
        }
        draw_fn = draw_map.get(state.go_state)
        if draw_fn:
            return draw_fn(screen, state, renderer)
        return []

    def handle_click(self, pos, state, rects) -> bool:
        if state.go_state == STATE_CHOICE:
            return self._handle_choice_click(pos, state, rects)

        if state.go_state == STATE_QUESTION:
            return self._handle_question_click(pos, state, rects)

        if state.go_state == STATE_RESULT_OK:
            state.game_over = False
            state.spawn_rescue_blocks()
            state.clear_question()
            state.go_state = STATE_GAME_OVER
            return True

        if state.go_state == STATE_RESULT_FAIL:
            state.__init__()
            return True

        return False

    def _draw_choice(self, screen, state, renderer) -> list[pygame.Rect]:
        cx = SCREEN_WIDTH // 2
        renderer.draw_centered(renderer.font_big, "Игра окончена!", (255, 80, 80), 220)
        renderer.draw_centered(renderer.font_med, f"Счёт: {state.score}", (200, 200, 200), 280)

        restart_btn = pygame.Rect(0, 0, 220, 52)
        restart_btn.center = (cx, 370)
        pygame.draw.rect(screen, (80, 200, 120), restart_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Начать заново", (20, 20, 25), 370)

        question_btn = pygame.Rect(0, 0, 260, 52)
        question_btn.center = (cx, 445)
        pygame.draw.rect(screen, (80, 130, 255), question_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Ответить на вопрос", (255, 255, 255), 445)

        return [restart_btn, question_btn]

    def _draw_loading(self, screen, state, renderer) -> list[pygame.Rect]:
        renderer.draw_centered(renderer.font_big, "Загрузка вопроса...", (255, 255, 255), 320)
        dots = "." * ((pygame.time.get_ticks() // 500) % 4)
        renderer.draw_centered(renderer.font_med, f"Пожалуйста, подождите{dots}", (200, 200, 200), 400)
        return []

    def _draw_question(self, screen, state, renderer) -> list[pygame.Rect]:
        cx = SCREEN_WIDTH // 2
        max_width = SCREEN_WIDTH - 100
        y = 150

        for line in renderer.wrap_text(state.question_text, renderer.font_med, max_width):
            renderer.draw_centered(renderer.font_med, line, (255, 255, 255), y)
            y += 32

        y = max(y + 30, 340)
        option_rects = []

        for option in state.options:
            lines = renderer.wrap_text(option, renderer.font_med, SCREEN_WIDTH - 120)
            height = max(44, len(lines) * 24 + 10)

            rect = pygame.Rect(0, 0, SCREEN_WIDTH - 80, height)
            rect.center = (cx, y + height // 2)
            pygame.draw.rect(screen, (70, 70, 90), rect, border_radius=8)

            line_y = rect.centery - (len(lines) - 1) * 12
            for line in lines:
                surf = renderer.font_med.render(line, True, (230, 230, 230))
                screen.blit(surf, surf.get_rect(center=(cx, line_y)))
                line_y += 24

            option_rects.append(rect)
            y += height + 10

        return option_rects

    def _draw_result_ok(self, screen, state, renderer) -> list[pygame.Rect]:
        renderer.draw_centered(renderer.font_big, "Правильно!", (80, 220, 100), 300)
        renderer.draw_centered(renderer.font_med, "Нажми, чтобы продолжить", (200, 200, 200), 370)
        return []

    def _draw_result_fail(self, screen, state, renderer) -> list[pygame.Rect]:
        renderer.draw_centered(renderer.font_big, "Неверно!", (255, 80, 80), 300)
        renderer.draw_centered(renderer.font_med, "Нажми, чтобы начать заново", (200, 200, 200), 370)
        return []

    def _handle_choice_click(self, pos, state, rects) -> bool:
        if len(rects) < 2:
            return False
        if rects[0].collidepoint(pos):
            state.__init__()
            return True
        if rects[1].collidepoint(pos):
            self._fetch(state)
            return True
        return False

    def _handle_question_click(self, pos, state, rects) -> bool:
        for i, rect in enumerate(rects):
            if rect.collidepoint(pos):
                state.selected_index = i
                state.go_state = (
                    STATE_RESULT_OK if i == state.correct_index else STATE_RESULT_FAIL
                )
                return True
        return False

    def _fetch(self, state):
        state.go_state = STATE_LOADING
        api_client.fetch_question_async(
            on_success=lambda q, o, c: self._on_success(state, q, o, c),
            on_error=lambda msg: self._on_error(state, msg)
        )

    def _on_success(self, state, question, options, correct_index):
        state.apply_question(question, options, correct_index)
        state.go_state = STATE_QUESTION

    def _on_error(self, state, error_msg):
        question, options, correct = api_client.make_error_question(error_msg)
        state.apply_question(question, options, correct)
        state.go_state = STATE_QUESTION
