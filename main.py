import pygame
from game_engine import Game


def main():
    pygame.init()
    pygame.display.set_caption("Lexa Blocks")
    Game().run()


if __name__ == "__main__":
    main()
