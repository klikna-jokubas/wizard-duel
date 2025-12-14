class StatusEffect:
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration

    def on_turn_start(self, owner, log: list[str]):
        pass

    def is_expired(self) -> bool:
        return self.duration <= 0


class PoisonEffect(StatusEffect):
    def __init__(self, damage_per_turn: int, duration: int):
        super().__init__("Poison", duration)
        self.damage_per_turn = damage_per_turn

    def on_turn_start(self, owner, log: list[str]):
        owner.take_damage(self.damage_per_turn)
        log.append(
            f"{owner.name} kenčia nuo nuodų! -{self.damage_per_turn} HP."
        )
        self.duration -= 1

class SilenceEffect(StatusEffect):
    def __init__(self, duration: int):
        super().__init__("Silence", duration)

    def on_turn_start(self, owner, log: list[str]):
        log.append(
            f"{owner.name} yra nutildytas ({self.duration} ėjimai liko)."
        )
        self.duration -= 1
