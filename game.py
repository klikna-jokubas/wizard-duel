import pygame

from settings import WIDTH, HEIGHT, FONT, BIG_FONT, WHITE, GREEN, RED
from spells import Spell
from player_wizard import PlayerWizard
from enemy_wizard import EnemyWizard
from characters import Character


class Game:
    def __init__(self):

        self.player: Character = PlayerWizard(
            "Player", 150, 260, (50, 80, 200), "player_mage.png"
        )

        self.enemy: Character = EnemyWizard(
            "Enemy", 750, 260, (200, 50, 50), "player_mage.png"
        )

        # --- Burtai ---
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

    # Input iš žaidėjo (polymorphism)

    def handle_player_input(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.__init__()
            return

        if self.current_turn == "player":
            finished = self.player.take_turn(self, event)

            if finished:
                self.check_game_over()

                if not self.game_over:
                    self.next_turn()
                    self.enemy.take_turn(self)
                    self.check_game_over()

                    if not self.game_over:
                        self.next_turn()

    # Žaidimo būsena

    def check_game_over(self):
        if not self.player.is_alive():
            self.game_over = True
            self.winner = self.enemy.name
            self.add_message("Tu pralaimėjai!")
        elif not self.enemy.is_alive():
            self.game_over = True
            self.winner = self.player.name
            self.add_message("Tu laimėjai!")

    # Piešimas

    def draw_spell_list(self, surface):
        y = HEIGHT - 160
        x = 40
        title = FONT.render("Tavo burtai (spausk 1,2,3...):", True, WHITE)
        surface.blit(title, (x, y))
        y += 25

        for i, spell in enumerate(self.player.spells):
            text = (
                f"{i+1}. {spell.name} "
                f"(Dmg:{spell.damage}, Heal:{spell.heal}, Mana:{spell.mana_cost})"
            )
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
        text_rect = text_surf.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 20)
        )
        surface.blit(text_surf, text_rect)

        info_surf = FONT.render(
            "Spausk R, kad pradėtum iš naujo", True, WHITE
        )
        info_rect = info_surf.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 20)
        )
        surface.blit(info_surf, info_rect)

    def draw(self, surface):
        surface.fill((15, 15, 30))

        self.player.draw(surface)
        self.enemy.draw(surface)

        self.draw_spell_list(surface)
        self.draw_log(surface)
        self.draw_game_over(surface)
