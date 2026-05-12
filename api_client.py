import json
import os
import random
import threading

import requests
from dotenv import load_dotenv

load_dotenv()

_API_KEY = os.getenv("DEEPSEEK_API_KEY")
_API_URL = "https://api.deepseek.com/v1/chat/completions"

_SYSTEM_PROMPT = "Ты генератор математических задач. Отвечай только валидным JSON."

_USER_PROMPT = (
    "Придумай НОВУЮ математическую задачу. "
    "Ответ СТРОГО в JSON:\n"
    '{"question": "вопрос", "options": ["A)", "B)", "C)", "D)"], "correct": 0}'
)


def fetch_question_async(on_success, on_error):
    thread = threading.Thread(target=_fetch_question, args=(on_success, on_error), daemon=True)
    thread.start()


def _fetch_question(on_success, on_error):
    try:
        data = _make_request()
        question, options, correct = _parse_response(data)
        on_success(question, options, correct)

    except requests.exceptions.Timeout:
        on_error("Таймаут соединения")

    except requests.exceptions.RequestException as e:
        on_error(f"Ошибка соединения: {e}")

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        on_error(f"Ошибка формата ответа: {e}")

    except Exception as e:
        on_error(f"Неизвестная ошибка: {e}")


def _make_request() -> dict:
    headers = {
        "Authorization": f"Bearer {_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": _USER_PROMPT},
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    response = requests.post(_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    return response.json()


def _parse_response(data: dict) -> tuple[str, list[str], int]:
    raw = data["choices"][0]["message"]["content"]
    raw = raw.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(raw)
    return parsed["question"], parsed["options"], int(parsed["correct"])


def make_error_question(error_msg: str) -> tuple[str, list[str], int]:
    question = f"Ошибка: {error_msg}. Попробуй ещё раз. ({random.randint(1, 100)})"
    options = ["A) Повторить", "B) Сдаться", "C) Выход", "D) 0"]
    return question, options, 0
