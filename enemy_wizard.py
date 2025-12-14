import random
from wizards import Wizard
from ai_strategy import DefaultAIStrategy

LOW_HP_THRESHOLD = 15


class EnemyWizard(Wizard):
    def take_turn(self, game, event=None):
        """
        AI pats nusprendžia, ką daryti
        """
        available_spells = [
            s for s in self.spells if s.mana_cost <= self.mana
        ]

        if not available_spells:
            game.add_message(f"{self.name} neturi mannos burtams!")
            return True

        self.strategy = DefaultAIStrategy()

