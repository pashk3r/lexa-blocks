import random

import pygame

import api_client
from base_plugin import BasePlugin
from constants import (
    SCREEN_WIDTH,
    STATE_GAME_OVER, STATE_CHOICE, STATE_LOADING,
    STATE_QUESTION, STATE_INPUT, STATE_FIND_ERROR,
    STATE_RESULT_OK, STATE_RESULT_FAIL,
    QUIZ_CHOICE, QUIZ_INPUT, QUIZ_FIND_ERROR,
)

_COLOR_NORMAL = (70, 70, 90)
_COLOR_HOVER = (90, 90, 120)
_COLOR_SELECTED = (180, 80, 80)


class QuizPlugin(BasePlugin):

    def __init__(self):
        self._hovered_step: int | None = None

    def on_game_over(self, state, renderer) -> bool:
        state.go_state = STATE_CHOICE
        return True

    def on_restart(self, state):
        state.go_state = STATE_GAME_OVER
        self._hovered_step = None

    def draw_overlay(self, screen, state, renderer) -> list[pygame.Rect]:
        draw_map = {
            STATE_CHOICE: self._draw_choice,
            STATE_LOADING: self._draw_loading,
            STATE_QUESTION: self._draw_question,
            STATE_INPUT: self._draw_input,
            STATE_FIND_ERROR: self._draw_find_error,
            STATE_RESULT_OK: self._draw_result_ok,
            STATE_RESULT_FAIL: self._draw_result_fail,
        }
        fn = draw_map.get(state.go_state)
        return fn(screen, state, renderer) if fn else []

    def _draw_choice(self, screen, state, renderer) -> list[pygame.Rect]:
        cx = SCREEN_WIDTH // 2
        renderer.draw_centered(renderer.font_big, "Игра окончена!", (255, 80, 80), 200)
        renderer.draw_centered(renderer.font_med, f"Счёт: {state.score}", (200, 200, 200), 258)

        restart_btn = pygame.Rect(0, 0, 220, 52)
        restart_btn.center = (cx, 330)
        pygame.draw.rect(screen, (80, 200, 120), restart_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Начать заново", (20, 20, 25), 330)

        q1_btn = pygame.Rect(0, 0, 260, 48)
        q1_btn.center = (cx, 400)
        pygame.draw.rect(screen, (80, 130, 255), q1_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Варианты ответа", (255, 255, 255), 400)

        q2_btn = pygame.Rect(0, 0, 260, 48)
        q2_btn.center = (cx, 460)
        pygame.draw.rect(screen, (80, 180, 220), q2_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Введи ответ", (255, 255, 255), 460)

        q3_btn = pygame.Rect(0, 0, 260, 48)
        q3_btn.center = (cx, 520)
        pygame.draw.rect(screen, (180, 100, 220), q3_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Найди ошибку", (255, 255, 255), 520)

        random_btn = pygame.Rect(0, 0, 260, 48)
        random_btn.center = (cx, 590)
        pygame.draw.rect(screen, (220, 150, 50), random_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Случайный вопрос", (255, 255, 255), 590)

        return [restart_btn, q1_btn, q2_btn, q3_btn, random_btn]

    def _draw_loading(self, screen, state, renderer) -> list[pygame.Rect]:
        renderer.draw_centered(renderer.font_big, "Загрузка...", (255, 255, 255), 320)
        dots = "." * ((pygame.time.get_ticks() // 500) % 4)
        renderer.draw_centered(renderer.font_med, f"Пожалуйста, подождите{dots}", (200, 200, 200),
                               390)
        return []

    def _draw_question(self, screen, state, renderer) -> list[pygame.Rect]:
        cx = SCREEN_WIDTH // 2
        max_w = SCREEN_WIDTH - 100
        y = 130

        renderer.draw_centered(renderer.font_small, "① Выбери правильный ответ", (150, 150, 200), y)
        y += 36

        for line in renderer.wrap_text(state.question_text, renderer.font_med, max_w):
            renderer.draw_centered(renderer.font_med, line, (255, 255, 255), y)
            y += 32

        y = max(y + 20, 320)
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

    def _draw_input(self, screen, state, renderer) -> list[pygame.Rect]:
        cx = SCREEN_WIDTH // 2
        max_w = SCREEN_WIDTH - 100
        y = 130

        renderer.draw_centered(renderer.font_small, "② Введи числовой ответ", (150, 200, 150), y)
        y += 36

        for line in renderer.wrap_text(state.question_text, renderer.font_med, max_w):
            renderer.draw_centered(renderer.font_med, line, (255, 255, 255), y)
            y += 32

        y = max(y + 30, 360)

        # Поле ввода
        field = pygame.Rect(0, 0, SCREEN_WIDTH - 80, 52)
        field.center = (cx, y)
        pygame.draw.rect(screen, (50, 50, 70), field, border_radius=8)
        pygame.draw.rect(screen, (120, 180, 255), field, width=2, border_radius=8)

        display = state.input_text if state.input_text else ""
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
        surf = renderer.font_med.render(display + cursor, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=field.center))

        y += 80

        confirm_btn = pygame.Rect(0, 0, 200, 50)
        confirm_btn.center = (cx, y)
        active = bool(state.input_text)
        color = (80, 200, 120) if active else (60, 80, 60)
        pygame.draw.rect(screen, color, confirm_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Подтвердить",
                               (20, 20, 25) if active else (100, 120, 100), y)

        renderer.draw_centered(
            renderer.font_small,
            "← Backspace для удаления",
            (120, 120, 140),
            y + 50
        )

        return [confirm_btn]

    def _draw_find_error(self, screen, state, renderer) -> list[pygame.Rect]:
        cx = SCREEN_WIDTH // 2
        y = 120

        renderer.draw_centered(renderer.font_small, "③ Найди ошибочный шаг", (200, 150, 220), y)
        y += 44

        step_rects = []
        mouse_pos = pygame.mouse.get_pos()

        for i, step in enumerate(state.error_steps):
            lines = renderer.wrap_text(step, renderer.font_med, SCREEN_WIDTH - 110)
            height = max(46, len(lines) * 24 + 12)

            rect = pygame.Rect(0, 0, SCREEN_WIDTH - 70, height)
            rect.center = (cx, y + height // 2)

            hovering = rect.collidepoint(mouse_pos)
            if hovering:
                self._hovered_step = i

            color = _COLOR_HOVER if hovering else _COLOR_NORMAL
            pygame.draw.rect(screen, color, rect, border_radius=8)

            num_surf = renderer.font_small.render(str(i + 1), True, (180, 180, 200))
            screen.blit(num_surf, (rect.left + 10, rect.centery - num_surf.get_height() // 2))

            line_y = rect.centery - (len(lines) - 1) * 12
            for line in lines:
                surf = renderer.font_med.render(line, True, (230, 230, 230))
                screen.blit(surf, surf.get_rect(center=(cx + 10, line_y)))
                line_y += 24

            step_rects.append(rect)
            y += height + 8

        return step_rects

    def _draw_result_ok(self, screen, state, renderer) -> list[pygame.Rect]:
        renderer.draw_centered(renderer.font_big, "Правильно!", (80, 220, 100), 300)
        renderer.draw_centered(renderer.font_med, "Нажми, чтобы продолжить", (200, 200, 200), 370)
        return []

    def _draw_result_fail(self, screen, state, renderer) -> list[pygame.Rect]:
        renderer.draw_centered(renderer.font_big, "Неверно!", (255, 80, 80), 280)

        hint = self._get_fail_hint(state)
        if hint:
            for i, line in enumerate(hint):
                renderer.draw_centered(renderer.font_med, line, (220, 180, 80), 340 + i * 28)

        renderer.draw_centered(renderer.font_med, "Нажми, чтобы начать заново", (200, 200, 200),
                               460)
        return []

    def _get_fail_hint(self, state) -> list[str]:
        match state.go_state:
            case _ if state.correct_answer:
                return [f"Правильный ответ: {state.correct_answer}"]
            case _ if state.error_steps:
                idx = state.error_step_index
                step = state.error_steps[idx]
                lines = [f"Ошибка в шаге {idx + 1}:"]
                # Обрезаем длинный текст
                if len(step) > 38:
                    lines.append(step[:38] + "…")
                else:
                    lines.append(step)
                return lines
            case _:
                return []

    def handle_click(self, pos, state, rects) -> bool:
        match state.go_state:
            case s if s == STATE_CHOICE:
                return self._handle_choice_click(pos, state, rects)
            case s if s == STATE_QUESTION:
                return self._handle_question_click(pos, state, rects)
            case s if s == STATE_INPUT:
                return self._handle_input_click(pos, state, rects)
            case s if s == STATE_FIND_ERROR:
                return self._handle_find_error_click(pos, state, rects)
            case s if s == STATE_RESULT_OK:
                state.game_over = False
                state.spawn_rescue_blocks()
                state.clear_question()
                state.go_state = STATE_GAME_OVER
                self._hovered_step = None
                return True
            case s if s == STATE_RESULT_FAIL:
                state.__init__()
                self._hovered_step = None
                return True
        return False

    def handle_keydown(self, event, state) -> bool:
        if state.go_state != STATE_INPUT:
            return False

        match event.key:
            case pygame.K_BACKSPACE:
                state.input_text = state.input_text[:-1]
            case pygame.K_RETURN | pygame.K_KP_ENTER:
                if state.input_text:
                    self._check_input_answer(state)
            case _ if event.unicode.isprintable() and event.unicode:
                if len(state.input_text) < 20:
                    state.input_text += event.unicode
        return True

    def _handle_choice_click(self, pos, state, rects) -> bool:
        if len(rects) < 5:
            return False
        restart, q1, q2, q3, rand = rects[:5]

        if restart.collidepoint(pos):
            state.__init__()
            return True
        if q1.collidepoint(pos):
            self._fetch(state, QUIZ_CHOICE)
            return True
        if q2.collidepoint(pos):
            self._fetch(state, QUIZ_INPUT)
            return True
        if q3.collidepoint(pos):
            self._fetch(state, QUIZ_FIND_ERROR)
            return True
        if rand.collidepoint(pos):
            self._fetch(state, random.choice([QUIZ_CHOICE, QUIZ_INPUT, QUIZ_FIND_ERROR]))
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

    def _handle_input_click(self, pos, state, rects) -> bool:
        if rects and rects[0].collidepoint(pos) and state.input_text:
            self._check_input_answer(state)
            return True
        return False

    def _handle_find_error_click(self, pos, state, rects) -> bool:
        for i, rect in enumerate(rects):
            if rect.collidepoint(pos):
                state.go_state = (
                    STATE_RESULT_OK if i == state.error_step_index else STATE_RESULT_FAIL
                )
                return True
        return False

    def _check_input_answer(self, state):
        # Нормализуем: убираем пробелы, сравниваем как строки
        got = state.input_text.strip()
        expected = state.correct_answer.strip()
        state.go_state = STATE_RESULT_OK if got == expected else STATE_RESULT_FAIL

    def _fetch(self, state, quiz_type: str):
        state.go_state = STATE_LOADING
        api_client.fetch_question_async(
            quiz_type=quiz_type,
            on_success=lambda qt, result: self._on_success(state, qt, result),
            on_error=lambda msg: self._on_error(state, msg, quiz_type),
        )

    def _on_success(self, state, quiz_type: str, result):
        match quiz_type:
            case "choice":
                question, options, correct = result
                state.apply_choice_question(question, options, correct)
                state.go_state = STATE_QUESTION
            case "input":
                question, answer = result
                state.apply_input_question(question, answer)
                state.go_state = STATE_INPUT
            case "find_error":
                steps, error_index = result
                state.apply_find_error_question(steps, error_index)
                state.go_state = STATE_FIND_ERROR

    def _on_error(self, state, error_msg: str, quiz_type: str):
        fallback_type, fallback_data = api_client.make_error_question(error_msg, quiz_type)
        self._on_success(state, fallback_type, fallback_data)
