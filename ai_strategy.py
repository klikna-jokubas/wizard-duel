from abc import ABC, abstractmethod
import random


class AIStrategy(ABC):
    @abstractmethod
    def choose_spell(self, wizard, enemy):
        pass


class DefaultAIStrategy(AIStrategy):
    def choose_spell(self, wizard, enemy):
        available_spells = [
            s for s in wizard.spells if s.mana_cost <= wizard.mana
        ]

        if not available_spells:
            return None

        if wizard.hp < 15:
            heal_spells = [s for s in available_spells if s.heal > 0]
            if heal_spells and random.random() < 0.6:
                return random.choice(heal_spells)

        return random.choice(available_spells)
