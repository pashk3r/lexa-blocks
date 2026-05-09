import os
import pygame
from game_engine import Game


def main():
    pygame.init()
    pygame.display.set_caption("Lexa Blocks")

    if os.path.exists("lexa.jpg"):
        pygame.display.set_icon(pygame.image.load("lexa.jpg"))

    Game().run()


if __name__ == "__main__":
    main()
