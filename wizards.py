import pygame
import os

from settings import FONT, WHITE, GREY, RED, BLUE
from effects import PoisonEffect, SilenceEffect
from characters import Character

MANA_REGEN = 2
ICE_FIRE_COMBO_BONUS = 5
POISON_DAMAGE = 3
POISON_DURATION = 3
SILENCE_DURATION = 2


class Wizard(Character):
    def __init__(self, name, x, y, color, sprite_path=None):
        super().__init__(name=name, max_hp=50)

        self._max_mana = 30
        self._mana = 30

        self.spells: list = []
        self._last_spell_name: str | None = None

        self.x = x
        self.y = y
        self.color = color
        self.width = 80
        self.height = 120

        self.sprite = None
        if sprite_path:
            self._load_sprite(sprite_path)

    # Encapsulation – getteriai

    @property
    def mana(self) -> int:
        return self._mana

    @property
    def max_mana(self) -> int:
        return self._max_mana

    def spend_mana(self, amount: int) -> bool:
        if self._mana < amount:
            return False
        self._mana -= amount
        return True

    def restore_mana(self, amount: int):
        self._mana += amount
        if self._mana > self._max_mana:
            self._mana = self._max_mana

    def add_spell(self, spell):
        self.spells.append(spell)

    def cast_spell(self, target: "Wizard", spell) -> str:
        if self.has_effect("Silence"):
            return f"{self.name} yra nutildytas ir negali naudoti burtų!"

        if not self.spend_mana(spell.mana_cost):
            return f"{self.name} bandė panaudoti {spell.name}, bet neturi pakankamai mannos!"

        log = [f"{self.name} panaudojo {spell.name}!"]

        if spell.name == "Fireball":
            target.add_effect(
                PoisonEffect(
                    damage_per_turn=POISON_DAMAGE,
                    duration=POISON_DURATION,
                )
            )

        if spell.name == "Silence Potion":
            target.add_effect(SilenceEffect(duration=SILENCE_DURATION))
            log.append(f"{target.name} yra nutildytas {SILENCE_DURATION} ėjimams!")

        combo_bonus = self._calculate_combo_bonus(spell)

        if spell.damage > 0:
            total_damage = spell.damage + combo_bonus
            target.take_damage(total_damage)
            log.append(f"-{total_damage} HP {target.name}.")
            if combo_bonus > 0:
                log.append(f"Kombo! +{combo_bonus} papildomos žalos.")

        if spell.heal > 0:
            self.heal(spell.heal)
            log.append(f"+{spell.heal} HP {self.name}.")

        self._last_spell_name = spell.name
        self.restore_mana(MANA_REGEN)

        return " ".join(log)

    def _calculate_combo_bonus(self, spell) -> int:
        if self._last_spell_name == "Ice Spike" and spell.name == "Fireball":
            return ICE_FIRE_COMBO_BONUS
        return 0

    # Polymorphism 

    def take_turn(self):
        """
        Realus elgesys apibrėžiamas Game / AI logikoje.
        Metodas reikalingas polymorphism + abstraction.
        """
        pass

    # Piešimas

    def draw(self, surface):
        if self.sprite:
            surface.blit(self.sprite, (self.x, self.y))
        else:
            pygame.draw.rect(
                surface,
                self.color,
                pygame.Rect(self.x, self.y, self.width, self.height),
            )

        name_surf = FONT.render(self.name, True, WHITE)
        surface.blit(name_surf, (self.x, self.y - 25))

        self._draw_bar(
            surface,
            self.hp,
            self.max_hp,
            self.x,
            self.y + self.height + 5,
            RED,
            "HP",
        )

        self._draw_bar(
            surface,
            self.mana,
            self.max_mana,
            self.x,
            self.y + self.height + 25,
            BLUE,
            "MP",
        )

    def _draw_bar(self, surface, value, max_value, x, y, color, label):
        bar_width = self.width
        bar_height = 12
        ratio = value / max_value if max_value > 0 else 0

        pygame.draw.rect(surface, GREY, (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, color, (x, y, int(bar_width * ratio), bar_height))

        text = FONT.render(f"{label}: {value}/{max_value}", True, WHITE)
        surface.blit(text, (x, y - 18))

    # Sprite

    def _load_sprite(self, sprite_path: str):
        full_path = os.path.join("assets", sprite_path)
        try:
            image = pygame.image.load(full_path).convert_alpha()
            self.sprite = pygame.transform.scale(
                image, (self.width, self.height)
            )
        except pygame.error as e:
            print(f"Nepavyko užkrauti sprite '{full_path}': {e}")
            self.sprite = None
