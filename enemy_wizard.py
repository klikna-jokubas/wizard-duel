import random
from wizards import Wizard

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

        spell = random.choice(available_spells)

        if self.hp < LOW_HP_THRESHOLD:
            heal_spells = [s for s in available_spells if s.heal > 0]
            if heal_spells and random.random() < 0.6:
                spell = random.choice(heal_spells)

        text = self.cast_spell(game.player, spell)
        game.add_message(text)
        return True
