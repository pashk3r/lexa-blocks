SCREEN_WIDTH = 435
SCREEN_HEIGHT = 750
GRID_SIZE = 8
CELL_SIZE = 45
MARGIN = 40
FPS = 60

SLOT_Y = 600
SLOT_X_START = 50
SLOT_SPACING = 130

COLORS = {
    "bg": (20, 20, 25),
    "grid": (40, 40, 50),
    "blocks": [(255, 80, 80), (80, 255, 80), (80, 80, 255), (255, 200, 50),
               (255, 80, 200)]
}

SHAPES = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0)]
]

STATE_GAME_OVER = "game_over"
STATE_CHOICE = "choice"
STATE_LOADING = "loading"
STATE_QUESTION = "question"
STATE_INPUT = "input"
STATE_MATCH = "match"
STATE_RESULT_OK = "result_ok"
STATE_RESULT_FAIL = "result_fail"

QUIZ_CHOICE = "choice"
QUIZ_INPUT = "input"
QUIZ_MATCH = "match"
