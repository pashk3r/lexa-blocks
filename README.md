# Проектирование Lexa-Blocks

**Ветка:** `design`  
**Статус:** проектирование (ожидаю уточнений от аналитика по пунктам, отмеченным `TODO`)

## Артефакты аналитика
- [Аналитический документ](https://github.com/pashk3r/lexa_blocks/blob/analysis/docs/analysis.md) — SADT‑диаграммы, сравнение с аналогами.

## Диаграммы (UML)
| Файл | Тип | Описание |
|------|-----|----------|
| `models/component-diagram.puml` | Компонентная | GameCore, EduModule, интерфейс IEduService |
| `models/class-diagram.puml` | Классов | Основные классы и их связи |
| `models/state-machine.puml` | Состояний | Состояния игры |

## Работа с диаграммами
- [Исходники](./models) (PlantUML).
- [Диаграммы в PNG](./generated) (закоммичены для быстрого просмотра).

## Спецификации
- [Игровые правила](./specs/game_rules.md) — очки, уровни, кубы, условие тупика.
- [Предположения](./specs/assumptions.md) — что доопределил сам.
