import sys
import os
import types
import pytest
from unittest.mock import MagicMock


def _setup_mocks():
    pygame_mock = types.ModuleType("pygame")
    pygame_mock.init = lambda: None
    pygame_mock.quit = lambda: None
    pygame_mock.display = MagicMock()
    pygame_mock.font = MagicMock()
    pygame_mock.font.SysFont = MagicMock(return_value=MagicMock())
    pygame_mock.Surface = MagicMock()
    pygame_mock.Rect = MagicMock(return_value=MagicMock())
    pygame_mock.draw = MagicMock()
    pygame_mock.time = MagicMock()
    pygame_mock.time.get_ticks = MagicMock(return_value=0)
    pygame_mock.SRCALPHA = 0
    pygame_mock.MOUSEBUTTONDOWN = 1
    pygame_mock.MOUSEMOTION = 2
    pygame_mock.QUIT = 3

    class _Vector2:
        def __init__(self, x_or_pair=0, y=None):
            if y is None:
                self.x, self.y = (x_or_pair[0], x_or_pair[1]) if hasattr(x_or_pair, '__getitem__') else (float(x_or_pair), 0.0)
            else:
                self.x, self.y = float(x_or_pair), float(y)
        def __sub__(self, other): return _Vector2(self.x - other.x, self.y - other.y)
        def __add__(self, other): return _Vector2(self.x + other.x, self.y + other.y)
        def __repr__(self): return f"Vector2({self.x}, {self.y})"

    pygame_mock.Vector2 = _Vector2

    sys.modules["pygame"] = pygame_mock
    sys.modules["dotenv"] = MagicMock()
    sys.modules["requests"] = MagicMock()

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)


_setup_mocks()

from board import Board
from blocks import Block
from game_state import GameState
from quiz_plugin import QuizPlugin


def make_block(shape, color=(255, 0, 0)):
    """Создать Block с заданной формой — правильный способ передачи в Board."""
    return Block(shape=shape, color=color, slot_pos=(0, 0))


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def empty_state():
    return GameState()


@pytest.fixture
def game_over_state():
    state = GameState()
    state.game_over = True
    return state


@pytest.fixture
def plugin():
    return QuizPlugin()


@pytest.fixture
def renderer():
    return MagicMock()


@pytest.fixture
def state_with_score():
    state = GameState()
    state.score = 150
    state.level = 2
    state.game_over = True
    return state
