import pytest

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wizards import Wizard
from spells import Spell
from effects import PoisonEffect, SilenceEffect


@pytest.fixture
def wizard_pair():
    wiz1 = Wizard("A", 0, 0, (0, 0, 0))
    wiz2 = Wizard("B", 0, 0, (0, 0, 0))
    return wiz1, wiz2


def test_damage_reduces_hp(wizard_pair):
    attacker, target = wizard_pair
    fireball = Spell("Fireball", damage=10, mana_cost=3)

    attacker.cast_spell(target, fireball)

    assert target.hp == target.max_hp - 10


def test_heal_does_not_exceed_max_hp(wizard_pair):
    wiz, _ = wizard_pair
    heal = Spell("Heal", heal=20, mana_cost=3)

    wiz.take_damage(10)
    wiz.cast_spell(wiz, heal)

    assert wiz.hp == wiz.max_hp


def test_poison_effect_damages_over_time(wizard_pair):
    wiz, _ = wizard_pair
    wiz.add_effect(PoisonEffect(damage_per_turn=3, duration=1))

    log = []
    wiz.process_effects_start_of_turn(log)

    assert wiz.hp == wiz.max_hp - 3


def test_silence_blocks_spell(wizard_pair):
    attacker, target = wizard_pair
    fireball = Spell("Fireball", damage=10, mana_cost=3)

    attacker.add_effect(SilenceEffect(duration=1))
    result = attacker.cast_spell(target, fireball)

    assert "nutildytas" in result
    assert target.hp == target.max_hp


def test_mana_is_spent_on_cast(wizard_pair):
    attacker, target = wizard_pair
    fireball = Spell("Fireball", damage=5, mana_cost=4)

    start_mana = attacker.mana
    attacker.cast_spell(target, fireball)

    assert attacker.mana < start_mana


def test_combo_bonus_applied(wizard_pair):
    attacker, target = wizard_pair
    ice = Spell("Ice Spike", damage=5, mana_cost=2)
    fire = Spell("Fireball", damage=10, mana_cost=3)

    attacker.cast_spell(target, ice)
    attacker.cast_spell(target, fire)

    assert target.hp == target.max_hp - 20
