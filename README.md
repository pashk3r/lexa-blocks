# Проектирование Lexa-Blocks

**Ветка:** `design`  
**Статус:** проектирование (13.05 получены артефакты от аналитика)

## Артефакты аналитика
- [Аналитический документ](https://github.com/pashk3r/lexa_blocks/blob/analysis/docs/analysis.md) — SADT‑диаграммы, сравнение с аналогами.
- [Глоссарий](https://github.com/pashk3r/lexa_blocks/blob/analysis/docs/glossary.md) — сущности и атрибуты.
- [Use Cases](https://github.com/pashk3r/lexa_blocks/blob/analysis/docs/usecases.md) — сценарии UC-1..UC-5.
- [SRS](https://github.com/pashk3r/lexa_blocks/blob/analysis/docs/srs.md) — требования G1..G9.

## Диаграммы (UML)
| Файл | Тип | Описание |
|------|-----|----------|
| `models/component-diagram.puml` | Компонентная | GameCore, EduModule, интерфейс IEduService |
| `models/class-diagram.puml` | Классов | Основные классы и их связи |
| `models/state-machine.puml` | Состояний | Состояния игры |
| `models/sequence_place_figure.puml` | Последовательности | Размещение фигуры → очистка линий → начисление очков |
| `models/sequence_loss_and_math.puml` | Последовательности | Тупик → вопрос через API → правильный/неправильный ответ |
| `models/sequence_use_save_cube.puml` | Последовательности | Использование спасательного куба 1×1 |

## Работа с диаграммами
- [Исходники](./models) (PlantUML).
- [Диаграммы в PNG](./generated) (для быстрого просмотра).
- [Описание диаграмм](./models/docs).

## Спецификации
- [Игровые правила](./specs/game_rules.md) — очки, уровни, кубы, условие тупика.
- [Предположения](./specs/assumptions.md) — что доопределил сам.
