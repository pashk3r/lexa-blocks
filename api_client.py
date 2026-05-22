import json
import os
import random
import threading

import requests
from dotenv import load_dotenv

load_dotenv()

_API_KEY = os.getenv("DEEPSEEK_API_KEY")
_API_URL = "https://api.deepseek.com/v1/chat/completions"

_SYSTEM_PROMPT = "Ты генератор вопросов по языку программирования Python. Отвечай только валидным JSON."

_PROMPT_CHOICE = (
    "Придумай НОВЫЙ вопрос по Python (синтаксис, встроенные функции, типы данных, ООП, "
    "стандартная библиотека — тему выбирай случайно). "
    "Вопрос формулируй на русском. В вариантах можно использовать код. "
    "Ответ СТРОГО в JSON:\n"
    '{"question": "вопрос", "options": ["A) ...", "B) ...", "C) ...", "D) ..."], "correct": 0}'
)

_PROMPT_INPUT = (
    "Придумай НОВЫЙ вопрос по Python, ответом на который является одно конкретное слово, "
    "число или короткое выражение (например: имя метода, ключевое слово, число). "
    "Вопрос формулируй на русском. "
    "Пример: 'Как называется метод для добавления элемента в конец списка?' → answer: 'append'. "
    "Ответ СТРОГО в JSON (answer — строка, строчными буквами, без скобок и пробелов по краям):\n"
    '{"question": "вопрос", "answer": "ответ"}'
)

_PROMPT_FIND_ERROR = (
    "Придумай короткий фрагмент Python-кода (4–6 строк) с пошаговым разбором того, что он делает. "
    "В одной из строк кода намеренно допусти синтаксическую или логическую ошибку. "
    "Каждый шаг — это одна строка кода или её объяснение. "
    "Все описания на русском. "
    "Ответ СТРОГО в JSON:\n"
    '{"steps": ["строка 1 кода или описание", "строка 2...", ...], "error_index": 2}'
)


def fetch_question_async(quiz_type: str, on_success, on_error):
    thread = threading.Thread(
        target=_fetch_question,
        args=(quiz_type, on_success, on_error),
        daemon=True
    )
    thread.start()


def _fetch_question(quiz_type: str, on_success, on_error):
    try:
        data = _make_request(quiz_type)
        result = _parse_response(quiz_type, data)
        on_success(quiz_type, result)

    except requests.exceptions.Timeout:
        on_error("Таймаут соединения")

    except requests.exceptions.RequestException as e:
        on_error(f"Ошибка соединения: {e}")

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        on_error(f"Ошибка формата ответа: {e}")

    except Exception as e:
        on_error(f"Неизвестная ошибка: {e}")


def _make_request(quiz_type: str) -> dict:
    prompt_map = {
        "choice": _PROMPT_CHOICE,
        "input": _PROMPT_INPUT,
        "find_error": _PROMPT_FIND_ERROR,
    }
    user_prompt = prompt_map[quiz_type]

    headers = {
        "Authorization": f"Bearer {_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 600,
    }

    response = requests.post(_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def _parse_response(quiz_type: str, data: dict):
    raw = data["choices"][0]["message"]["content"]
    raw = raw.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(raw)

    match quiz_type:
        case "choice":
            return parsed["question"], parsed["options"], int(parsed["correct"])
        case "input":
            return parsed["question"], str(parsed["answer"])
        case "find_error":
            return parsed["steps"], int(parsed["error_index"])


def make_error_question(error_msg: str, quiz_type: str = "choice"):
    tag = random.randint(1, 100)
    match quiz_type:
        case "input":
            return "input", (
                f"Ошибка загрузки ({tag}). Как называется функция, "
                "возвращающая длину списка?",
                "len"
            )
        case "find_error":
            steps = [
                "nums = [1, 2, 3]",
                "# Хотим напечатать каждый элемент",
                f"for i in range(4):  # ошибка (тег {tag})",
                "    print(nums[i])",
            ]
            return "find_error", (steps, 2)
        case _:
            question = f"Ошибка загрузки ({tag}). Какой тип возвращает type([])?",
            options = ["A) list", "B) dict", "C) tuple", "D) set"]
            return "choice", (question, options, 0)
