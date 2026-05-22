# Bug Report — Lexa-Blocks

**Дата:** 22-05-2026  
**Тестировщик:** [egorka000](https://github.com/egorka000)  
**Ветка:** `testing`  
**Адресат:** программисты (ветка `development`)  

---

## Итоговая таблица дефектов

| ID | Приоритет | Файл | Строка | Тест | Статус |
|----|-----------|------|--------|------|--------|
| BUG-01 | 🔴 P1 | `board.py` | 58 | TC-12b, TC-12c | Открыт |
| BUG-02 | 🟠 P2 | `game_state.py` | 37 | TC-20b | Открыт |
| BUG-03 | 🟡 P3 | `game_state.py` | 96 | TC-23b | Открыт |
| BUG-04 | 🟠 P2 | `board.py` | 30 | TC-25b | Открыт |

> BUG-01 фиксируется двумя тестами (TC-12b и TC-12c) — оба подтверждают одну и ту же проблему при разном количестве линий.

---

## BUG-01 — Формула очков при 3+ одновременных линиях даёт квадратичный рост

**Приоритет:** 🔴 P1 — Критический  
**Компонент:** `board.py`, метод `_clear_lines()`, строка 54 
**Ответственный:** программист основной игры  
**Тесты:** TC-12b (`test_TC12b_three_lines_score_bug`), TC-12c (`test_TC12c_four_lines_score_bug`)

**Требование (SRS G3):** при одновременной очистке нескольких линий очки суммируются линейно: 1 линия = 10, 2 = 20, 3 = 30, 4 = 40.

**Фактическое поведение:**

| Линий | Ожидается (SRS) | Фактически (код) |
|-------|-----------------|------------------|
| 1 | 10 | 10 ✅ |
| 2 | 20 | 20 ✅ |
| 3 | 30 | **60** ❌ |
| 4 | 40 | **120** ❌ |

**Код с ошибкой (`board.py`, строка 58):**
```python
# НЕВЕРНО — квадратичный рост:
return lines * 10 * max(1, lines - 1)
# При lines=3: 3 * 10 * max(1, 2) = 60
# При lines=4: 4 * 10 * max(1, 3) = 120
```

**Исправление:**
```python
# ВЕРНО — линейная сумма по SRS:
return lines * 10
```

**Как воспроизвести:** заполнить 3 строки подряд и разместить фигуру, завершающую все три. Счёт вырастет на 60 вместо 30.

---

## BUG-02 — spawn_rescue_blocks() заменяет всю руку вместо добавления кубов

**Приоритет:** 🟠 P2 — Высокий  
**Компонент:** `game_state.py`, метод `spawn_rescue_blocks()`, строка 41  
**Ответственный:** программист основной игры  
**Тест:** TC-20b (`test_TC20b_rescue_blocks_lose_previous_hand`)

**Требование (SRS G9):** «игра сразу продолжается с того же места» — счёт и поле не меняются. Следовательно, фигуры в руке игрока также должны сохраняться.

**Фактическое поведение:** если перед тупиком у игрока оставались 1–2 неразмещённые фигуры, после правильного ответа они полностью заменяются тремя кубами 1×1. Игрок теряет свои фигуры.

**Код с ошибкой (`game_state.py`, строка 37):**
```python
# НЕВЕРНО — полная замена:
def spawn_rescue_blocks(self):
    self.blocks_in_hand = [          # ← перезаписывает старые фигуры
        Block([(0, 0)], ...)
        for i in range(3)
    ]
```

**Исправление:**
```python
# ВЕРНО — добавление к существующей руке:
def spawn_rescue_blocks(self):
    rescue = [
        Block(
            [(0, 0)],
            random.choice(COLORS["blocks"]),
            (SLOT_X_START + i * SLOT_SPACING, SLOT_Y)
        )
        for i in range(3)
    ]
    self.blocks_in_hand.extend(rescue)
```

**Как воспроизвести:**
1. Разместить 1 из 3 фигур (в руке остаётся 2).
2. Довести поле до тупика.
3. Ответить правильно на вопрос.
4. Наблюдать: в руке 3 куба 1×1 вместо ожидаемых 2 фигур + 3 куба.

---

## BUG-03 — clear_question() сбрасывает correct_index в 0 вместо None

**Приоритет:** 🟡 P3 — Средний  
**Компонент:** `game_state.py`, метод `clear_question()`, строка 104  
**Ответственный:** программист обучающей части  
**Тест:** TC-23b (`test_TC23b_clear_question_correct_index_not_reset`)

**Проблема:** после `clear_question()` атрибут `correct_index` равен `0`. Если обработчик клика вызовется в состоянии без активного вопроса, нажатие на первый вариант ответа (индекс `0`) будет засчитано как правильный — хотя вопроса нет. `selected_index` при этом корректно сбрасывается в `None`, создавая несимметричное поведение.

**Код с ошибкой (`game_state.py`, строки 90–96):**
```python
def clear_question(self):
    self.question_text = ""
    self.options = []
    self.correct_index = 0       # ← небезопасное значение
    self.selected_index = None   # ← правильно сброшен
```

**Исправление:**
```python
def clear_question(self):
    self.question_text = ""
    self.options = []
    self.correct_index = None    # ← безопасное значение
    self.selected_index = None
```

Дополнительно добавить защиту в `_handle_question_click`:
```python
if state.correct_index is None:
    return False
```

---

## BUG-04 — board.place() молча перезаписывает занятые ячейки

**Приоритет:** 🟠 P2 — Высокий  
**Компонент:** `board.py`, метод `place()`, строка 31  
**Ответственный:** программист основной игры  
**Тест:** TC-25b (`test_TC25b_place_overwrites_occupied_cell`)

**Проблема:** прямой вызов `board.place()` на уже занятую ячейку не выбрасывает ошибку и не возвращает `False` — он молча перезаписывает цвет ячейки. В текущей архитектуре `GameState` защищает от этого через предварительный вызов `can_place()`, но `Board` сам по себе небезопасен при прямом использовании.

**Код с ошибкой (`board.py`, строка 30):**
```python
def place(self, block, gx, gy):
    for dx, dy in block.shape:
        # Нет проверки — занятая ячейка будет перезаписана:
        self.grid[gy + dy][gx + dx] = block.color
```

**Исправление:**
```python
def place(self, block, gx, gy):
    for dx, dy in block.shape:
        r, c = gy + dy, gx + dx
        if self.grid[r][c] is not None:
            raise ValueError(
                f"Board.place(): ячейка ({c},{r}) уже занята. "
                f"Вызовите can_place() перед place()."
            )
        self.grid[r][c] = block.color
    placed_points = len(block.shape)
    line_points = self._clear_lines()
    return placed_points + line_points
```

**Как воспроизвести:**
```python
board = Board()
block_a = make_block([(0,0)], color=(255, 0, 0))
block_b = make_block([(0,0)], color=(0, 0, 255))
board.place(block_a, 0, 0)
board.place(block_b, 0, 0)        # перезаписывает без ошибки
print(board.grid[0][0])           # (0, 0, 255) — данные испорчены
```
