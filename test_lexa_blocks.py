"""
Тестовый скрипт — Lexa-Blocks
Дата: 22-05-2026
Фреймворк: pytest

"""

import pytest
from unittest.mock import MagicMock, patch

from constants import (
    GRID_SIZE,
    STATE_CHOICE, STATE_LOADING,
    STATE_QUESTION, STATE_RESULT_OK, STATE_RESULT_FAIL, STATE_GAME_OVER,
)
from game_state import GameState
from board import Board
from blocks import Block


# ---------------------------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ---------------------------------------------------------------------------

def make_block(shape, color=(255, 0, 0)):
    """Правильный способ создать Block для передачи в Board-методы."""
    return Block(shape=shape, color=color, slot_pos=(0, 0))


def make_full_row(board, row: int):
    color = (255, 0, 0)
    for col in range(GRID_SIZE):
        board.grid[row][col] = color


def make_full_col(board, col: int):
    color = (0, 255, 0)
    for row in range(GRID_SIZE):
        board.grid[row][col] = color


def cell_is_free(board, row, col) -> bool:
    return not board.grid[row][col]


def cell_is_occupied(board, row, col) -> bool:
    return bool(board.grid[row][col])


def fill_board_except(board, free_positions: list):
    color = (100, 100, 100)
    free_set = set(free_positions)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if (r, c) not in free_set:
                board.grid[r][c] = color


# ---------------------------------------------------------------------------
# БЛОК 1: ИГРОВОЕ ПОЛЕ — TC-01, TC-02
# ---------------------------------------------------------------------------

class TestField:

    def test_TC01_grid_size_is_8(self):
        """TC-01: Размер поля должен быть 8×8."""
        assert GRID_SIZE == 8

    def test_TC02_initial_field_all_cells_free(self, board):
        """TC-02: После создания Board все 64 ячейки свободны."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                assert cell_is_free(board, r, c), f"Ячейка ({r},{c}) должна быть свободна"


# ---------------------------------------------------------------------------
# БЛОК 2: РАЗМЕЩЕНИЕ ФИГУР — TC-03 — TC-08
# ---------------------------------------------------------------------------

class TestPlacement:

    def test_TC03_can_place_single_cube_on_empty_cell(self, board):
        """TC-03: Одиночный куб можно разместить на пустую ячейку."""
        block = make_block([(0, 0)])
        assert board.can_place(block, 3, 3) is True
        board.place(block, 3, 3)
        assert cell_is_occupied(board, 3, 3)

    def test_TC04_cannot_place_on_occupied_cell(self, board):
        """TC-04: Нельзя разместить фигуру на занятую ячейку."""
        block = make_block([(0, 0)])
        board.place(block, 3, 3)
        assert board.can_place(block, 3, 3) is False

    def test_TC05_cannot_place_outside_border(self, board):
        """TC-05: Горизонтальная линия 3×1 за правой границей отклоняется."""
        block = make_block([(0, 0), (1, 0), (2, 0)])
        assert board.can_place(block, 7, 0) is False

    def test_TC06_place_2x2_square(self, board):
        """TC-06: Квадрат 2×2 занимает все 4 ячейки."""
        block = make_block([(0, 0), (1, 0), (0, 1), (1, 1)], color=(0, 0, 255))
        board.place(block, 0, 0)
        assert cell_is_occupied(board, 0, 0)
        assert cell_is_occupied(board, 0, 1)
        assert cell_is_occupied(board, 1, 0)
        assert cell_is_occupied(board, 1, 1)

    def test_TC07_initial_panel_has_3_figures(self, empty_state):
        """TC-07: В начале игры в панели ровно 3 фигуры."""
        assert len(empty_state.blocks_in_hand) == 3

    def test_TC08_new_set_spawned_after_placing_all_three(self, empty_state):
        """TC-08: После очистки руки spawn_blocks() заполняет её снова 3 фигурами. [PASS ожидается]"""
        empty_state.blocks_in_hand.clear()
        empty_state.spawn_blocks()
        assert len(empty_state.blocks_in_hand) == 3

    def test_TC06b_place_does_not_accept_color_kwarg(self, board):
        """TC-06b: board.place() не принимает color= """
        with pytest.raises(TypeError, match="unexpected keyword argument"):
            board.place([(0, 0)], 0, 0, color=(255, 0, 0))


# ---------------------------------------------------------------------------
# БЛОК 3: ОЧИСТКА ЛИНИЙ И ОЧКИ — TC-09 — TC-14
# ---------------------------------------------------------------------------

class TestLinesAndScore:

    def test_TC09_full_row_is_cleared(self, board):
        """TC-09: Полностью заполненная строка очищается."""
        make_full_row(board, 0)
        board._clear_lines()
        for c in range(GRID_SIZE):
            assert cell_is_free(board, 0, c)

    def test_TC10_full_col_is_cleared(self, board):
        """TC-10: Полностью заполненный столбец очищается."""
        make_full_col(board, 0)
        board._clear_lines()
        for r in range(GRID_SIZE):
            assert cell_is_free(board, r, 0)

    def test_TC11_one_line_gives_10_points(self, board):
        """TC-11: Одна заполненная строка даёт 10 очков."""
        make_full_row(board, 0)
        points = board._clear_lines()
        assert points == 10

    def test_TC12_two_lines_give_20_points(self, board):
        """TC-12: Две линии одновременно = 20 очков по SRS G3."""
        make_full_row(board, 0)
        make_full_row(board, 1)
        points = board._clear_lines()
        assert points == 20, f"Ожидалось 20 очков за 2 линии, получено {points}"

    def test_TC12b_three_lines_score_bug(self, board):
        """TC-12b: Три линии одновременно = 30 очков по SRS G3."""
        make_full_row(board, 0)
        make_full_row(board, 1)
        make_full_row(board, 2)
        points = board._clear_lines()
        assert points == 30, (
            f"BUG-01: SRS требует 30 очков за 3 линии, "
            f"код вернул {points}. "
            f"Формула board.py:55: lines * 10 * max(1, lines-1) даёт квадратичный рост. "
            f"Исправление: заменить на lines * 10"
        )

    def test_TC12c_four_lines_score_bug(self, board):
        """TC-12c: Четыре линии одновременно = 40 очков по SRS G3."""
        make_full_row(board, 0)
        make_full_row(board, 1)
        make_full_col(board, 0)
        make_full_col(board, 1)
        points = board._clear_lines()
        assert points == 40, (
            f"BUG-01: SRS требует 40 очков за 4 линии, "
            f"код вернул {points}. Игрок получает в 3 раза больше очков."
        )

    def test_TC13_level_increases_at_100_points(self, empty_state):
        """TC-13: Уровень повышается при достижении 100 очков."""
        empty_state.score = 99
        empty_state._add_score(1)
        assert empty_state.level == 2

    def test_TC14_progress_50_points_equals_50_percent(self, empty_state):
        """TC-14: 50 очков = 50% прогресса (score % 100)."""
        empty_state._add_score(50)
        assert empty_state.score % 100 == 50


# ---------------------------------------------------------------------------
# БЛОК 4: УСЛОВИЕ ТУПИКА — TC-15, TC-16
# ---------------------------------------------------------------------------

class TestGameOver:

    def test_TC15_game_over_when_no_moves(self, empty_state):
        """TC-15: _is_game_over() = True когда поле заблокировано."""
        fill_board_except(empty_state.board, [])
        assert empty_state._is_game_over() is True

    def test_TC16_no_game_over_when_moves_available(self, empty_state):
        """TC-16: _is_game_over() = False на пустом поле."""
        assert empty_state._is_game_over() is False


# ---------------------------------------------------------------------------
# БЛОК 5: ПЕРЕХОДЫ СОСТОЯНИЙ ВИКТОРИНЫ — TC-17 — TC-23
# ---------------------------------------------------------------------------

class TestQuizPlugin:

    def test_TC17_on_game_over_sets_state_choice(self, plugin, game_over_state, renderer):
        """TC-17: on_game_over переводит в STATE_CHOICE."""
        plugin.on_game_over(game_over_state, renderer)
        assert game_over_state.go_state == STATE_CHOICE

    def test_TC18_fetch_sets_state_loading(self, plugin, game_over_state):
        """TC-18: _fetch переводит в STATE_LOADING."""
        with patch("api_client.fetch_question_async") as mock_fetch:
            mock_fetch.return_value = None
            plugin._fetch(game_over_state)
        assert game_over_state.go_state == STATE_LOADING

    def test_TC19_on_success_sets_state_question(self, plugin, game_over_state):
        """TC-19: _on_success задаёт вопрос и переходит в STATE_QUESTION."""
        plugin._on_success(
            game_over_state,
            "Сколько будет 2+2?",
            ["A)3", "B)4", "C)5", "D)6"],
            1
        )
        assert game_over_state.go_state == STATE_QUESTION
        assert game_over_state.question_text == "Сколько будет 2+2?"
        assert len(game_over_state.options) == 4
        assert game_over_state.correct_index == 1

    def test_TC20_correct_answer_gives_rescue_blocks(self, plugin, game_over_state):
        """TC-20: Правильный ответ → STATE_RESULT_OK → game_over=False → 3 куба."""
        game_over_state.go_state = STATE_QUESTION
        game_over_state.correct_index = 1
        game_over_state.options = ["A)3", "B)4", "C)5", "D)6"]
        original_score = game_over_state.score

        rects = [MagicMock() for _ in range(4)]
        for i, rect in enumerate(rects):
            rect.collidepoint = MagicMock(return_value=(i == 1))

        plugin._handle_question_click((0, 0), game_over_state, rects)
        assert game_over_state.go_state == STATE_RESULT_OK

        plugin.handle_click((0, 0), game_over_state, [])
        assert game_over_state.game_over is False
        assert len(game_over_state.blocks_in_hand) == 3
        assert game_over_state.score == original_score

    def test_TC20b_rescue_blocks_lose_previous_hand(self, plugin, game_over_state):
        """TC-20b: Старые фигуры сохраняются после правильного ответа"""
        from blocks import Block
        from constants import SHAPES, COLORS, SLOT_X_START, SLOT_SPACING, SLOT_Y
        import random

        # Добавляем 2 фигуры в руку перед спасением
        existing = [
            Block(SHAPES[0], COLORS["blocks"][0], (SLOT_X_START, SLOT_Y)),
            Block(SHAPES[1], COLORS["blocks"][1], (SLOT_X_START + SLOT_SPACING, SLOT_Y)),
        ]
        game_over_state.blocks_in_hand = existing[:]

        game_over_state.go_state = STATE_QUESTION
        game_over_state.correct_index = 0
        game_over_state.options = ["A)42", "B)0", "C)1", "D)2"]

        rects = [MagicMock() for _ in range(4)]
        rects[0].collidepoint = MagicMock(return_value=True)
        for r in rects[1:]:
            r.collidepoint = MagicMock(return_value=False)

        plugin._handle_question_click((0, 0), game_over_state, rects)
        plugin.handle_click((0, 0), game_over_state, [])

        # После правильного ответа рука должна содержать 2 старые + 3 новые = 5 фигур
        # Или как минимум старые фигуры должны сохраниться
        old_shapes = [b.shape for b in existing]
        current_shapes = [b.shape for b in game_over_state.blocks_in_hand]

        assert any(s in current_shapes for s in old_shapes), (
            "BUG-02: spawn_rescue_blocks() заменяет всю руку. "
            "SRS G9 требует продолжения 'с того же места' — старые фигуры потеряны. "
            "game_state.py:37: self.blocks_in_hand = [...] нужно заменить на extend()"
        )

    def test_TC21_wrong_answer_resets_game(self, plugin, state_with_score):
        """TC-21: Неправильный ответ → STATE_RESULT_FAIL → полный сброс."""
        state_with_score.go_state = STATE_QUESTION
        state_with_score.correct_index = 1
        state_with_score.options = ["A)3", "B)4", "C)5", "D)6"]

        rects = [MagicMock() for _ in range(4)]
        for i, rect in enumerate(rects):
            rect.collidepoint = MagicMock(return_value=(i == 0))

        plugin._handle_question_click((0, 0), state_with_score, rects)
        assert state_with_score.go_state == STATE_RESULT_FAIL

        plugin.handle_click((0, 0), state_with_score, [])
        assert state_with_score.score == 0
        assert state_with_score.level == 1
        assert state_with_score.game_over is False

    def test_TC22_restart_button_resets_game(self, plugin, state_with_score):
        """TC-22: Кнопка «Начать заново» в STATE_CHOICE сбрасывает игру."""
        state_with_score.go_state = STATE_CHOICE

        restart_rect = MagicMock()
        restart_rect.collidepoint = MagicMock(return_value=True)
        question_rect = MagicMock()
        question_rect.collidepoint = MagicMock(return_value=False)

        plugin._handle_choice_click(
            (0, 0), state_with_score, [restart_rect, question_rect]
        )
        assert state_with_score.score == 0
        assert state_with_score.level == 1
        assert state_with_score.game_over is False

    def test_TC23_api_error_shows_fake_question(self, plugin, game_over_state):
        """TC-23: При ошибке API система показывает фейковый вопрос (задокументированное поведение).
        
        Задокументировано в quiz_plugin.py: _on_error вызывает make_error_question()
        и переходит в STATE_QUESTION. Кнопки «Повторить» нет — это архитектурное решение.
        """
        plugin._on_error(game_over_state, "Таймаут соединения")
        assert game_over_state.go_state == STATE_QUESTION

    def test_TC23b_clear_question_correct_index_not_reset(self, empty_state):
        """TC-23b: clear_question()` сбрасывает `correct_index` в None."""
        empty_state.apply_question("Вопрос?", ["A)1", "B)2", "C)3", "D)4"], correct_index=2)
        empty_state.clear_question()
        assert empty_state.correct_index is None, (
            "BUG-03: clear_question() устанавливает correct_index=0 вместо None. "
            "game_state.py:96: self.correct_index = 0 → self.correct_index = None"
        )


# ---------------------------------------------------------------------------
# БЛОК 6: СПАСАТЕЛЬНЫЕ КУБЫ — TC-24, TC-25
# ---------------------------------------------------------------------------

class TestRescueCubes:

    def test_TC24_spawn_rescue_blocks_gives_3_single_cubes(self, empty_state):
        """TC-24: spawn_rescue_blocks() создаёт 3 куба с формой [(0,0)]. [PASS ожидается]"""
        empty_state.spawn_rescue_blocks()
        assert len(empty_state.blocks_in_hand) == 3
        for block in empty_state.blocks_in_hand:
            assert block.shape == [(0, 0)], f"Ожидался одиночный куб [(0,0)], получен: {block.shape}"

    def test_TC25_rescue_cube_clears_line_when_completing_row(self, board):
        """TC-25: Спасательный куб завершает строку → очистка + минимум 10 очков."""
        for c in range(7):
            board.grid[0][c] = (255, 0, 0)
        block = make_block([(0, 0)], color=(0, 255, 0))
        board.place(block, 7, 0)
        for c in range(GRID_SIZE):
            assert cell_is_free(board, 0, c), f"Ячейка (0,{c}) должна быть очищена"

    def test_TC25b_place_overwrites_occupied_cell(self, board):
        """TC-25b: board.place()` не перезаписывает занятые ячейки"""
        block_a = make_block([(0, 0)], color=(255, 0, 0))
        block_b = make_block([(0, 0)], color=(0, 0, 255))
        board.place(block_a, 0, 0)
        original_color = board.grid[0][0]

        board.place(block_b, 0, 0)  # перезаписываем занятую ячейку

        assert board.grid[0][0] == original_color, (
            "BUG-04: board.place() молча перезаписал занятую ячейку. "
            "board.py:30: нет проверки занятости перед grid[gy+dy][gx+dx] = block.color. "
            "Добавить: if self.grid[gy+dy][gx+dx]: raise ValueError('Cell occupied')"
        )


# ---------------------------------------------------------------------------
# БЛОК 7: ГРАНИЧНЫЕ ЗНАЧЕНИЯ — TC-26 — TC-28
# ---------------------------------------------------------------------------

class TestBoundary:

    def test_TC26_place_in_corner_0_0(self, board):
        """TC-26: Размещение одиночного куба в угол (col=0, row=0)."""
        block = make_block([(0, 0)])
        assert board.can_place(block, 0, 0) is True
        board.place(block, 0, 0)
        assert cell_is_occupied(board, 0, 0)

    def test_TC27_place_in_corner_7_7(self, board):
        """TC-27: Размещение одиночного куба в угол (col=7, row=7)."""
        block = make_block([(0, 0)])
        assert board.can_place(block, 7, 7) is True
        board.place(block, 7, 7)
        assert cell_is_occupied(board, 7, 7)

    def test_TC28_apply_and_clear_question(self, empty_state):
        """TC-28: apply_question и clear_question работают корректно."""
        empty_state.apply_question(
            "Сколько будет 3*3?", ["A)6", "B)9", "C)12", "D)3"], 1
        )
        assert empty_state.question_text == "Сколько будет 3*3?"
        assert len(empty_state.options) == 4
        assert empty_state.correct_index == 1

        empty_state.clear_question()
        assert empty_state.question_text == ""
        assert empty_state.options == []
