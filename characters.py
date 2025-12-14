from abc import ABC, abstractmethod
from effects import StatusEffect

class Character(ABC):
    def __init__(self, name: str, max_hp: int):
        self._name = name
        self._max_hp = max_hp
        self._hp = max_hp
        self._effects: list[StatusEffect] = []

    # --- Encapsulation (getteriai) ---

    @property
    def name(self) -> str:
        return self._name

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def max_hp(self) -> int:
        return self._max_hp

    def is_alive(self) -> bool:
        return self._hp > 0

    # --- Bendra logika ---

    def take_damage(self, amount: int):
        self._hp -= amount
        if self._hp < 0:
            self._hp = 0

    def heal(self, amount: int):
        self._hp += amount
        if self._hp > self._max_hp:
            self._hp = self._max_hp

    def add_effect(self, effect: StatusEffect):
        self._effects.append(effect)

    def has_effect(self, name: str) -> bool:
        return any(e.name == name and not e.is_expired() for e in self._effects)

    def process_effects_start_of_turn(self, log: list[str]):
        for effect in list(self._effects):
            effect.on_turn_start(self, log)
        self._effects = [e for e in self._effects if not e.is_expired()]

    # --- Abstrakcija ---
    @abstractmethod
    def take_turn(self):
        """Ką personažas daro savo ėjimo metu"""
        pass
