class Spell:
    def __init__(self, name, damage=0, heal=0, mana_cost=0):
        self.name = name
        self.damage = damage
        self.heal = heal
        self.mana_cost = mana_cost

    def __repr__(self):
        return (
            f"{self.name} (Dmg:{self.damage}, Heal:{self.heal}, Mana:{self.mana_cost})"
        )
