import sys
import pygame

from settings import WIDTH, HEIGHT
from game import Game


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wizard Duel")

    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_player_input(event)

        game.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
