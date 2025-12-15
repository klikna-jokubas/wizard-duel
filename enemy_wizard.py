from wizards import Wizard
from ai_strategy import DefaultAIStrategy


class EnemyWizard(Wizard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.strategy = DefaultAIStrategy()

    def take_turn(self, game, event=None):
        spell = self.strategy.choose_spell(self, game.player)

        if spell is None:
            game.add_message(f"{self.name} neturi mannos burtams!")
            return True

        text = self.cast_spell(game.player, spell)
        game.add_message(text)
        return True
