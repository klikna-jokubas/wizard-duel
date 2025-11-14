import random
import pygame

from settings import WIDTH, HEIGHT, FONT, BIG_FONT, WHITE, GREEN, RED
from wizards import Wizard
from spells import Spell


class Game:
    def __init__(self):
        self.player = Wizard(
            "Player", 150, 260, (50, 80, 200), "player_mage.png"
        )  # mėlynas
        self.enemy = Wizard(
            "Enemy", 750, 260, (200, 50, 50), "player_mage.png"
        )  # raudonas

        # burtai
        fireball = Spell("Fireball", damage=10, heal=0, mana_cost=4)
        ice_spike = Spell("Ice Spike", damage=6, heal=0, mana_cost=3)
        heal = Spell("Heal", damage=0, heal=7, mana_cost=5)
        lightning = Spell("Lightning Bolt", damage=12, heal=0, mana_cost=6)
        silence_potion = Spell("Silence Potion", damage=0, heal=0, mana_cost=4)

        for wiz in (self.player, self.enemy):
            wiz.add_spell(fireball)
            wiz.add_spell(ice_spike)
            wiz.add_spell(heal)
            wiz.add_spell(lightning)
            wiz.add_spell(silence_potion)

        self.current_turn = "player"
        self.message_log: list[str] = ["Kova prasidėjo!"]

        self.player.process_effects_start_of_turn(self.message_log)

        self.game_over = False
        self.winner = None

    # --- PAGALBINIAI METODAI ---

    def add_message(self, msg: str):
        self.message_log.append(msg)
        if len(self.message_log) > 6:
            self.message_log.pop(0)

    def next_turn(self):
        if self.current_turn == "player":
            self.current_turn = "enemy"
            self.enemy.process_effects_start_of_turn(self.message_log)
        else:
            self.current_turn = "player"
            self.player.process_effects_start_of_turn(self.message_log)

    # --- ENEMY AI ---

    def enemy_turn(self):
        if self.game_over:
            return

        available_spells = [
            s for s in self.enemy.spells if s.mana_cost <= self.enemy.mana
        ]
        if not available_spells:
            self.add_message(f"{self.enemy.name} neturi mannos burtams!")
            return

        spell = random.choice(available_spells)

        # jei mažai HP, dažniau heal
        if self.enemy.hp < 15:
            heal_spells = [s for s in available_spells if s.heal > 0]
            if heal_spells and random.random() < 0.6:
                spell = random.choice(heal_spells)

        text = self.enemy.cast_spell(self.player, spell)
        self.add_message(text)

    # --- INPUT IŠ ŽAIDĖJO ---

    def handle_player_input(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.game_over:
            if event.key == pygame.K_r:
                self.__init__()
            return

        # jeigu ne žaidėjo eilė – ignoruojam klavišus
        if self.current_turn != "player":
            return

        if pygame.K_1 <= event.key <= pygame.K_9:
            index = event.key - pygame.K_1
            if index < len(self.player.spells):
                spell = self.player.spells[index]
                text = self.player.cast_spell(self.enemy, spell)
                self.add_message(text)
                self.check_game_over()

                if not self.game_over:
                    self.next_turn()
                    self.enemy_turn()
                    self.check_game_over()

                if not self.game_over:
                    self.next_turn()

    # --- ŽAIDIMO BŪSENA ---

    def check_game_over(self):
        if not self.player.is_alive():
            self.game_over = True
            self.winner = self.enemy.name
            self.add_message("Tu pralaimėjai!")
        elif not self.enemy.is_alive():
            self.game_over = True
            self.winner = self.player.name
            self.add_message("Tu laimėjai!")

    # --- PIEŠIMAS ---

    def draw_spell_list(self, surface):
        y = HEIGHT - 160
        x = 40
        title = FONT.render("Tavo burtai (spausk 1,2,3...):", True, WHITE)
        surface.blit(title, (x, y))
        y += 25

        for i, spell in enumerate(self.player.spells):
            text = f"{i+1}. {spell.name} (Dmg:{spell.damage}, Heal:{spell.heal}, Mana:{spell.mana_cost})"
            surf = FONT.render(text, True, WHITE)
            surface.blit(surf, (x, y))
            y += 20

    def draw_log(self, surface):
        x = 500
        y = HEIGHT - 180
        title = FONT.render("Log:", True, WHITE)
        surface.blit(title, (x, y))
        y += 25

        for line in self.message_log:
            surf = FONT.render(line, True, WHITE)
            surface.blit(surf, (x, y))
            y += 20

    def draw_game_over(self, surface):
        if not self.game_over:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        text = f"Game Over! Winner: {self.winner}"
        text_surf = BIG_FONT.render(
            text,
            True,
            GREEN if self.winner == self.player.name else RED,
        )
        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        surface.blit(text_surf, text_rect)

        info_surf = FONT.render("Spausk R, kad pradėtum iš naujo", True, WHITE)
        info_rect = info_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        surface.blit(info_surf, info_rect)

    def draw(self, surface):
        surface.fill((15, 15, 30))

        self.player.draw(surface)
        self.enemy.draw(surface)

        self.draw_spell_list(surface)
        self.draw_log(surface)
        self.draw_game_over(surface)
