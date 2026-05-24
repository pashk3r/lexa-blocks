import os
import sys
import pygame
from game_engine import Game


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    pygame.init()
    pygame.display.set_caption("Lexa Blocks")

    icon_path = resource_path("lexa.jpg")
    if os.path.exists(icon_path):
        pygame.display.set_icon(pygame.image.load(icon_path))

    from quiz_plugin import QuizPlugin
    Game(plugin=QuizPlugin()).run()


if __name__ == "__main__":
    main()
