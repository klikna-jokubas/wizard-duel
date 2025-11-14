import pygame
import os

from settings import FONT, WHITE, GREY, RED, BLUE
from effects import PoisonEffect, StatusEffect


class Wizard:
    def __init__(self, name, x, y, color, sprite_path=None):
        self.name = name
        self.max_hp = 50
        self.hp = 50
        self.max_mana = 30
        self.mana = 30
        self.spells = []

        # piešimui
        self.x = x
        self.y = y
        self.color = color
        self.width = 80
        self.height = 120

        self.last_spell_name = None

        self.effects: list[StatusEffect] = []

        self.sprite = None
        if sprite_path is not None:
            full_path = os.path.join("assets", sprite_path)
            try:
                image = pygame.image.load(full_path).convert_alpha()
                self.sprite = pygame.transform.scale(image, (self.width, self.height))
            except pygame.error as e:
                print(f"Nepavyko užkrauti sprite '{full_path}': {e}")
                self.sprite = None

    # --- LOGIKA ---

    def add_spell(self, spell):
        self.spells.append(spell)

    def is_alive(self) -> bool:
        return self.hp > 0

    def cast_spell(self, target: "Wizard", spell) -> str:

        if self.has_effect("Silence"):
            return f"{self.name} yra nutildytas ir negali naudoti burtų!"
        
        if spell.name == "Fireball":
            target.add_effect(PoisonEffect(damage_per_turn=3, duration=3))

        if self.mana < spell.mana_cost:
            return f"{self.name} bandė panaudoti {spell.name}, bet neturi pakankamai mannos!"

        self.mana -= spell.mana_cost
        text_parts = [f"{self.name} panaudojo {spell.name}!"]

        combo_bonus = 0
        if self.last_spell_name == "Ice Spike" and spell.name == "Fireball":
            combo_bonus = 5

        if spell.damage > 0:
            total_damage = spell.damage + combo_bonus
            target.hp -= total_damage
            if target.hp < 0:
                target.hp = 0
            text_parts.append(f"-{total_damage} HP {target.name}.")
            if combo_bonus > 0:
                text_parts.append(f"Kombo! +{combo_bonus} papildomos žalos.")

        # GYDYMAS
        if spell.heal > 0:
            self.hp += spell.heal
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            text_parts.append(f"+{spell.heal} HP {self.name}.")

        self.last_spell_name = spell.name
        self.mana += 2

        return " ".join(text_parts)

    # --- PIEŠIMAS ---

    def draw(self, surface):
        if self.sprite is not None:
            surface.blit(self.sprite, (self.x, self.y))
        else:
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(surface, self.color, rect)

        name_surf = FONT.render(self.name, True, WHITE)
        surface.blit(name_surf, (self.x, self.y - 25))

        self._draw_bar(
            surface, self.hp, self.max_hp, self.x, self.y + self.height + 5, RED, "HP"
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

    # --- STATUS EFEKTAI ---

    def add_effect(self, effect: StatusEffect):
        self.effects.append(effect)

    def has_effect(self, name: str) -> bool:
        return any(e.name == name and not e.is_expired() for e in self.effects)

    def process_effects_start_of_turn(self, log: list[str]):
        for effect in list(self.effects):
            effect.on_turn_start(self, log)
        self.effects = [e for e in self.effects if not e.is_expired()]
