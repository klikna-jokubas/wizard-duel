import pygame
from wizards import Wizard


class PlayerWizard(Wizard):
    def take_turn(self, game, event=None):
        if event is None or event.type != pygame.KEYDOWN:
            return False

        if pygame.K_1 <= event.key <= pygame.K_9:
            index = event.key - pygame.K_1
            if index < len(self.spells):
                spell = self.spells[index]
                text = self.cast_spell(game.enemy, spell)
                game.add_message(text)
                return True

        return False
