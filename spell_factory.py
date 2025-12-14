from spells import Spell


class SpellFactory:
    @staticmethod
    def create_default_spells():
        return [
            Spell("Fireball", damage=10, heal=0, mana_cost=4),
            Spell("Ice Spike", damage=6, heal=0, mana_cost=3),
            Spell("Heal", damage=0, heal=7, mana_cost=5),
            Spell("Lightning Bolt", damage=12, heal=0, mana_cost=6),
            Spell("Silence Potion", damage=0, heal=0, mana_cost=4),
        ]
