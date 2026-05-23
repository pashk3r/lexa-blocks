# Проектирование Lexa-Blocks

**Ветка:** `design`  
**Статус:** проектирование завершено (диаграммы и спецификации согласованы с кодом)

## Артефакты аналитика
- [Аналитический документ](https://github.com/pashk3r/lexa_blocks/blob/analysis/docs/analysis.md) — SADT‑диаграммы, сравнение с аналогами.
- [Глоссарий](https://github.com/pashk3r/lexa_blocks/blob/analysis/docs/glossary.md) — сущности и атрибуты.
- [Use Cases](https://github.com/pashk3r/lexa_blocks/blob/analysis/docs/usecases.md) — сценарии UC-1..UC-5.
- [SRS](https://github.com/pashk3r/lexa_blocks/blob/analysis/docs/srs.md) — требования G1..G9.

## Диаграммы (UML)
| Файл | Тип | Описание |
|------|-----|----------|
| `models/component-diagram.puml` | Компонентная | GameCore, QuizPlugin (плагин спасения), api_client, DeepSeek API |
| `models/class-diagram.puml` | Классов | Все классы ядра, плагина, модуля api_client и перечисления состояний |
| `models/state-machine.puml` | Состояний | Полный автомат: от STATE_GAME_OVER до STATE_RESULT_OK/FAIL с учётом STATE_INPUT и STATE_FIND_ERROR |
| `models/sequence_place_figure.puml` | Последовательности | Размещение фигуры → очистка линий → начисление очков (UC-1) |
| `models/sequence_loss_and_math.puml` | Последовательности | Тупик → выбор типа викторины → запрос API → правильный/неправильный ответ (UC-4) |
| `models/sequence_use_save_cube.puml` | Последовательности | Использование спасательного куба 1×1 (UC-5) |

**Примечание:** диаграммы поддерживают три типа викторины: выбор варианта (choice), ввод ответа (input) и «найди ошибку» (find_error).

## Работа с диаграммами
- [Исходники](./models) (PlantUML)
- [Диаграммы в PNG](./generated) (для быстрого просмотра)
- [Описание диаграмм](./models/docs/diagrams_description.md) — подробное текстовое описание каждой диаграммы

## Спецификации
- [Игровые правила](./specs/game_rules.md) — правила игры, очки, уровни, кубы, тупик и **три типа вопросов по Python**
- [Предположения](./specs/assumptions.md) — устарело, все предположения заменены утверждёнными требованиями

## Руководство для разработчиков
- Все классы, методы и связи должны строго соответствовать [диаграмме классов](./models/class-diagram.puml).
- Логика переходов между экранами — по [диаграмме состояний](./models/state-machine.puml).
- При реализации викторины опирайтесь на [диаграмму последовательности UC-4](./models/sequence_loss_and_math.puml).
- Для интеграции с API используйте модуль `api_client` — его функции и сигнатуры описаны в диаграмме классов.
