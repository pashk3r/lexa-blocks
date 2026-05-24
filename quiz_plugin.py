import random

import pygame

import api_client
from base_plugin import BasePlugin
from constants import (
    SCREEN_WIDTH,
    STATE_GAME_OVER, STATE_CHOICE, STATE_LOADING,
    STATE_QUESTION, STATE_INPUT, STATE_MATCH,
    STATE_RESULT_OK, STATE_RESULT_FAIL,
    QUIZ_CHOICE, QUIZ_INPUT, QUIZ_MATCH,
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
            STATE_INPUT: self._draw_input,
            STATE_MATCH: self._draw_match,
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
        pygame.draw.rect(screen, (200, 120, 60), q3_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Соответствие", (255, 255, 255), 520)

        rand_btn = pygame.Rect(0, 0, 260, 48)
        rand_btn.center = (cx, 580)
        pygame.draw.rect(screen, (220, 150, 50), rand_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Случайный вопрос", (255, 255, 255), 580)

        return [restart_btn, q1_btn, q2_btn, q3_btn, rand_btn]

    def _draw_loading(self, screen, state, renderer) -> list[pygame.Rect]:
        renderer.draw_centered(renderer.font_big, "Загрузка...", (255, 255, 255), 320)
        dots = "." * ((pygame.time.get_ticks() // 500) % 4)
        renderer.draw_centered(renderer.font_med, f"Пожалуйста, подождите{dots}", (200, 200, 200), 390)
        return []

    def _draw_question(self, screen, state, renderer) -> list[pygame.Rect]:
        cx = SCREEN_WIDTH // 2
        max_w = SCREEN_WIDTH - 100
        y = 130

        renderer.draw_centered(renderer.font_small, "Выбери правильный ответ", (150, 150, 200), y)
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
        y = 130

        renderer.draw_centered(renderer.font_small, "Введи ответ", (150, 200, 150), y)
        y += 36

        for line in renderer.wrap_text(state.question_text, renderer.font_med, SCREEN_WIDTH - 100):
            renderer.draw_centered(renderer.font_med, line, (255, 255, 255), y)
            y += 32

        y = max(y + 30, 360)

        field = pygame.Rect(0, 0, SCREEN_WIDTH - 80, 52)
        field.center = (cx, y)
        pygame.draw.rect(screen, (50, 50, 70), field, border_radius=8)
        pygame.draw.rect(screen, (120, 180, 255), field, width=2, border_radius=8)
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
        surf = renderer.font_med.render(state.input_text + cursor, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=field.center))

        y += 80
        active = bool(state.input_text)
        confirm_btn = pygame.Rect(0, 0, 200, 50)
        confirm_btn.center = (cx, y)
        pygame.draw.rect(screen, (80, 200, 120) if active else (60, 80, 60), confirm_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Подтвердить",
                               (20, 20, 25) if active else (100, 120, 100), y)
        renderer.draw_centered(renderer.font_small, "← Backspace для удаления", (120, 120, 140), y + 50)
        return [confirm_btn]

    def _draw_match(self, screen, state, renderer) -> list[pygame.Rect]:
        cx = SCREEN_WIDTH // 2
        col_w = (SCREEN_WIDTH - 30) // 2
        pad = 5
        line_h = 18
        HEADER_Y = 108
        TABLE_TOP = 128
        BOTTOM_RESERVE = 118

        renderer.draw_centered(
            renderer.font_small, "Соедини левый столбец с правым", (255, 200, 100), HEADER_Y
        )

        def row_lines(text, max_w):
            return renderer.wrap_text(text, renderer.font_small, max_w - pad * 2)

        row_heights = [
            max(len(row_lines(l, col_w)), len(row_lines(r, col_w))) * line_h + pad * 2
            for l, r in zip(state.match_left, state.match_right)
        ]

        available = (750 - BOTTOM_RESERVE) - TABLE_TOP - (len(row_heights) - 1) * 3
        total_h = sum(row_heights)
        scale = min(1.0, available / total_h) if total_h > 0 else 1.0
        row_heights = [max(int(h * scale), line_h + pad) for h in row_heights]

        y = TABLE_TOP
        for left_item, right_item, h in zip(state.match_left, state.match_right, row_heights):
            left_rect = pygame.Rect(4, y, col_w - 2, h)
            pygame.draw.rect(screen, (40, 60, 90), left_rect, border_radius=6)

            right_rect = pygame.Rect(cx + 2, y, col_w - 2, h)
            pygame.draw.rect(screen, (60, 40, 80), right_rect, border_radius=6)

            for item, rect, color in [
                (left_item, left_rect, (180, 220, 255)),
                (right_item, right_rect, (255, 200, 150)),
            ]:
                lines = row_lines(item, col_w)
                ty = y + h // 2 - (len(lines) * line_h) // 2
                for line in lines:
                    surf = renderer.font_small.render(line, True, color)
                    screen.blit(surf, surf.get_rect(midleft=(rect.left + pad, ty + line_h // 2)))
                    ty += line_h

            y += h + 3

        field_y = 750 - BOTTOM_RESERVE + 10
        btn_y = 750 - 38

        renderer.draw_centered(renderer.font_small, "Введи ответ: a1b2c3d4", (150, 150, 170), field_y - 14)

        field = pygame.Rect(0, 0, SCREEN_WIDTH - 120, 40)
        field.center = (cx, field_y + 20)
        pygame.draw.rect(screen, (50, 50, 70), field, border_radius=8)
        pygame.draw.rect(screen, (255, 200, 100), field, width=2, border_radius=8)
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
        surf = renderer.font_med.render(state.match_input + cursor, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=field.center))

        active = len(state.match_input) >= len(state.match_left) * 2
        confirm_btn = pygame.Rect(0, 0, 200, 40)
        confirm_btn.center = (cx, btn_y)
        pygame.draw.rect(screen, (80, 200, 120) if active else (60, 80, 60), confirm_btn, border_radius=10)
        renderer.draw_centered(renderer.font_med, "Подтвердить", (20, 20, 25) if active else (100, 120, 100), btn_y)
        return [confirm_btn]

    def _draw_result_ok(self, screen, state, renderer) -> list[pygame.Rect]:
        renderer.draw_centered(renderer.font_big, "Правильно!", (80, 220, 100), 300)
        renderer.draw_centered(renderer.font_med, "Нажми, чтобы продолжить", (200, 200, 200), 370)
        return []

    def _draw_result_fail(self, screen, state, renderer) -> list[pygame.Rect]:
        renderer.draw_centered(renderer.font_big, "Неверно!", (255, 80, 80), 280)
        hint = self._get_fail_hint(state)
        for i, line in enumerate(hint):
            renderer.draw_centered(renderer.font_med, line, (220, 180, 80), 340 + i * 28)
        renderer.draw_centered(renderer.font_med, "Нажми, чтобы начать заново", (200, 200, 200), 460)
        return []

    def _get_fail_hint(self, state) -> list[str]:
        if state.correct_answer:
            return [f"Правильный ответ: {state.correct_answer}"]
        if state.match_answer:
            return [f"Правильный ответ: {state.match_answer}"]
        return []

    def handle_click(self, pos, state, rects) -> bool:
        match state.go_state:
            case s if s == STATE_CHOICE:
                return self._handle_choice_click(pos, state, rects)
            case s if s == STATE_QUESTION:
                return self._handle_question_click(pos, state, rects)
            case s if s == STATE_INPUT:
                return self._handle_input_click(pos, state, rects)
            case s if s == STATE_MATCH:
                return self._handle_match_click(pos, state, rects)
            case s if s == STATE_RESULT_OK:
                state.game_over = False
                has_rescue_cubes = any(block.shape == [(0, 0)] for block in state.blocks_in_hand)
                if has_rescue_cubes:
                    old_blocks = state.blocks_in_hand[:]
                    state.spawn_rescue_blocks()
                    state.blocks_in_hand.extend(old_blocks)
                else:
                    state.spawn_rescue_blocks()
                state.clear_question()
                state.go_state = STATE_GAME_OVER
                return True
            case s if s == STATE_RESULT_FAIL:
                state.__init__()
                return True
        return False

    def handle_keydown(self, event, state) -> bool:
        if state.go_state == STATE_MATCH:
            return self._handle_match_keydown(event, state)
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
        if len(rects) < 1:
            return False
        restart = rects[0]
        if restart.collidepoint(pos):
            state.__init__()
            return True
        if len(rects) < 5:
            return False
        q1, q2, q3, rand = rects[1:5]
        if q1.collidepoint(pos):
            self._fetch(state, QUIZ_CHOICE)
            return True
        if q2.collidepoint(pos):
            self._fetch(state, QUIZ_INPUT)
            return True
        if q3.collidepoint(pos):
            self._fetch(state, QUIZ_MATCH)
            return True
        if rand.collidepoint(pos):
            self._fetch(state, random.choice([QUIZ_CHOICE, QUIZ_INPUT, QUIZ_MATCH]))
            return True
        return False

    def _handle_question_click(self, pos, state, rects) -> bool:
        for i, rect in enumerate(rects):
            if rect.collidepoint(pos):
                state.selected_index = i
                state.go_state = STATE_RESULT_OK if i == state.correct_index else STATE_RESULT_FAIL
                return True
        return False

    def _handle_input_click(self, pos, state, rects) -> bool:
        if rects and rects[0].collidepoint(pos) and state.input_text:
            self._check_input_answer(state)
            return True
        return False

    def _handle_match_click(self, pos, state, rects) -> bool:
        if rects and rects[0].collidepoint(pos):
            got = state.match_input.strip().lower()
            expected = state.match_answer.strip().lower()
            state.go_state = STATE_RESULT_OK if got == expected else STATE_RESULT_FAIL
            return True
        return False

    def _handle_match_keydown(self, event, state) -> bool:
        max_len = len(state.match_left) * 2
        match event.key:
            case pygame.K_BACKSPACE:
                state.match_input = state.match_input[:-1]
            case pygame.K_RETURN | pygame.K_KP_ENTER:
                if len(state.match_input) >= max_len:
                    got = state.match_input.strip().lower()
                    expected = state.match_answer.strip().lower()
                    state.go_state = STATE_RESULT_OK if got == expected else STATE_RESULT_FAIL
            case _ if event.unicode.isprintable() and event.unicode:
                if len(state.match_input) < max_len:
                    state.match_input += event.unicode.lower()
        return True

    def _check_input_answer(self, state):
        got = state.input_text.strip()
        expected = state.correct_answer.strip()
        state.go_state = STATE_RESULT_OK if got == expected else STATE_RESULT_FAIL

    def _fetch(self, state, quiz_type: str = "choice"):
        state.go_state = STATE_LOADING
        api_client.fetch_question_async(
            quiz_type=quiz_type,
            on_success=lambda qt, result: self._on_success(state, qt, result),
            on_error=lambda msg: self._on_error(state, msg, quiz_type),
        )

    def _on_success(self, state, quiz_type_or_question, result_or_options=None, correct_index=None):
        if result_or_options is not None and correct_index is not None:
            question = quiz_type_or_question
            options = result_or_options
            state.apply_choice_question(question, options, correct_index)
            state.go_state = STATE_QUESTION
            return

        quiz_type = quiz_type_or_question
        result = result_or_options
        match quiz_type:
            case "choice":
                question, options, correct = result
                state.apply_choice_question(question, options, correct)
                state.go_state = STATE_QUESTION
            case "input":
                question, answer = result
                state.apply_input_question(question, answer)
                state.go_state = STATE_INPUT
            case "match":
                left, right, answer = result
                state.apply_match_question(left, right, answer)
                state.go_state = STATE_MATCH

    def _on_error(self, state, error_msg: str, quiz_type: str = "choice"):
        fallback_type, fallback_data = api_client.make_error_question(error_msg, quiz_type)
        self._on_success(state, fallback_type, fallback_data)
