# Test Report — Lexa-Blocks

**Дата:** 22-05-2026  
**Тестировщик:** [egorka000](https://github.com/egorka000)  
**Ветка:** `testing`  
**Тестируемая ветка:** `development`  

---

## 1. Сводка

| Показатель | Значение |
|------------|----------|
| Всего тест-кейсов | 34 |
| ✅ Пройдено | 29 |
| ❌ Упало (реальные дефекты) | 5 |
| 🔴 Критических дефектов (P1) | 1 (BUG-01, подтверждён двумя тестами) |
| 🟠 Высоких дефектов (P2) | 2 (BUG-02, BUG-04) |
| 🟡 Средних дефектов (P3) | 1 (BUG-03) |

---

## 2. Результаты по тест-кейсам

### Блок 1 — Игровое поле

| ID | Название | Тест в скрипте | Результат |
|----|----------|----------------|-----------|
| TC-01 | Размер поля 8×8 | `test_TC01_grid_size_is_8` | ✅ PASS |
| TC-02 | Все ячейки свободны при старте | `test_TC02_initial_field_all_cells_free` | ✅ PASS |

### Блок 2 — Размещение фигур

| ID | Название | Тест в скрипте | Результат |
|----|----------|----------------|-----------|
| TC-03 | Размещение куба на свободную ячейку | `test_TC03_can_place_single_cube_on_empty_cell` | ✅ PASS |
| TC-04 | Отклонение на занятую ячейку | `test_TC04_cannot_place_on_occupied_cell` | ✅ PASS |
| TC-05 | Отклонение за границей поля | `test_TC05_cannot_place_outside_border` | ✅ PASS |
| TC-06 | Размещение квадрата 2×2 | `test_TC06_place_2x2_square` | ✅ PASS |
| TC-06b | `place()` не принимает `color=` | `test_TC06b_place_does_not_accept_color_kwarg` | ✅ PASS |
| TC-07 | В панели 3 фигуры в начале | `test_TC07_initial_panel_has_3_figures` | ✅ PASS |
| TC-08 | Новый набор после очистки руки | `test_TC08_new_set_spawned_after_placing_all_three` | ✅ PASS |

### Блок 3 — Очистка линий и очки

| ID | Название | Тест в скрипте | Результат |
|----|----------|----------------|-----------|
| TC-09 | Очистка заполненной строки | `test_TC09_full_row_is_cleared` | ✅ PASS |
| TC-10 | Очистка заполненного столбца | `test_TC10_full_col_is_cleared` | ✅ PASS |
| TC-11 | 1 линия = 10 очков | `test_TC11_one_line_gives_10_points` | ✅ PASS |
| TC-12 | 2 линии = 20 очков | `test_TC12_two_lines_give_20_points` | ✅ PASS |
| TC-12b | **3 линии = 30 очков** | `test_TC12b_three_lines_score_bug` | ❌ FAIL → **BUG-01** |
| TC-12c | **4 линии = 40 очков** | `test_TC12c_four_lines_score_bug` | ❌ FAIL → **BUG-01** |
| TC-13 | Уровень повышается при 100 очках | `test_TC13_level_increases_at_100_points` | ✅ PASS |
| TC-14 | Прогресс: 50 очков = 50% | `test_TC14_progress_50_points_equals_50_percent` | ✅ PASS |

### Блок 4 — Условие тупика

| ID | Название | Тест в скрипте | Результат |
|----|----------|----------------|-----------|
| TC-15 | `_is_game_over()` = True при заблокированном поле | `test_TC15_game_over_when_no_moves` | ✅ PASS |
| TC-16 | `_is_game_over()` = False на пустом поле | `test_TC16_no_game_over_when_moves_available` | ✅ PASS |

### Блок 5 — Переходы состояний викторины

| ID | Название | Тест в скрипте | Результат |
|----|----------|----------------|-----------|
| TC-17 | `on_game_over` → STATE_CHOICE | `test_TC17_on_game_over_sets_state_choice` | ✅ PASS |
| TC-18 | `_fetch` → STATE_LOADING | `test_TC18_fetch_sets_state_loading` | ✅ PASS |
| TC-19 | `_on_success` → STATE_QUESTION | `test_TC19_on_success_sets_state_question` | ✅ PASS |
| TC-20 | Правильный ответ → 3 куба, game_over=False | `test_TC20_correct_answer_gives_rescue_blocks` | ✅ PASS |
| TC-20b | **Старые фигуры сохраняются после правильного ответа** | `test_TC20b_rescue_blocks_lose_previous_hand` | ❌ FAIL → **BUG-02** |
| TC-21 | Неправильный ответ → полный сброс | `test_TC21_wrong_answer_resets_game` | ✅ PASS |
| TC-22 | «Начать заново» → сброс игры | `test_TC22_restart_button_resets_game` | ✅ PASS |
| TC-23 | Ошибка API → фейковый вопрос (задокументировано) | `test_TC23_api_error_shows_fake_question` | ✅ PASS |
| TC-23b | **`clear_question()` сбрасывает `correct_index` в None** | `test_TC23b_clear_question_correct_index_not_reset` | ❌ FAIL → **BUG-03** |

### Блок 6 — Спасательные кубы

| ID | Название | Тест в скрипте | Результат |
|----|----------|----------------|-----------|
| TC-24 | `spawn_rescue_blocks()` создаёт 3 куба 1×1 | `test_TC24_spawn_rescue_blocks_gives_3_single_cubes` | ✅ PASS |
| TC-25 | Куб завершает строку → очистка + очки | `test_TC25_rescue_cube_clears_line_when_completing_row` | ✅ PASS |
| TC-25b | **`board.place()` не перезаписывает занятые ячейки** | `test_TC25b_place_overwrites_occupied_cell` | ❌ FAIL → **BUG-04** |

### Блок 7 — Граничные значения

| ID | Название | Тест в скрипте | Результат |
|----|----------|----------------|-----------|
| TC-26 | Размещение в угол (gx=0, gy=0) | `test_TC26_place_in_corner_0_0` | ✅ PASS |
| TC-27 | Размещение в угол (gx=7, gy=7) | `test_TC27_place_in_corner_7_7` | ✅ PASS |
| TC-28 | `apply_question` / `clear_question` | `test_TC28_apply_and_clear_question` | ✅ PASS |

---

## 3. Найденные дефекты

| ID | Приоритет | Компонент | Строка | Краткое описание | Тест |
|----|-----------|-----------|--------|------------------|------|
| BUG-01 | 🔴 P1 | `board.py` | 58 | Квадратичная формула очков при 3+ линиях | TC-12b, TC-12c |
| BUG-02 | 🟠 P2 | `game_state.py` | 37 | `spawn_rescue_blocks()` заменяет всю руку | TC-20b |
| BUG-03 | 🟡 P3 | `game_state.py` | 96 | `clear_question()` не сбрасывает `correct_index` в `None` | TC-23b |
| BUG-04 | 🟠 P2 | `board.py` | 30 | `board.place()` молча перезаписывает занятые ячейки | TC-25b |

Подробное описание каждого дефекта — в `bug-report.md`.

---

## 4. Покрытие модулей

| Модуль | Покрытие |
|--------|----------|
| `board.py` | ✅ Высокое — все публичные методы покрыты |
| `game_state.py` | ✅ Высокое — очки, уровень, spawn, вопросы, переходы |
| `quiz_plugin.py` | ✅ Высокое — все состояния и переходы покрыты |
| `api_client.py` | 🟡 Среднее — мокируется, протестирован через `QuizPlugin` |
| `blocks.py` | 🟡 Низкое — используется косвенно через `Board` и `GameState` |
| `renderer.py` | ❌ Не покрыт — рендеринг вне области тестирования |
| `event_handler.py` | ❌ Не покрыт — обработка событий мыши вне области тестирования |

---

## 5. Выводы

Основная игровая механика (поле, очистка одной-двух линий, переходы состояний викторины) работает корректно. Выявлено 4 дефекта в 5 упавших тестов.

**BUG-01** является критическим: квадратичная формула очков проявляется в каждой игровой сессии при одновременной очистке 3+ линий и нарушает игровой баланс.

**Рекомендация:** до мержа в `main` обязательно закрыть BUG-01 и BUG-04. После исправлений повторно запустить тесты TC-12b, TC-12c, TC-20b, TC-23b, TC-25b, они должны перейти в PASS.
