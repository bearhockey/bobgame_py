import random


def hit_check(accuracy, accuracy_stat, evade_stat, bonus):
    dice = accuracy + accuracy_stat - evade_stat + bonus
    if dice < 1:
        dice = 1
    successes = 0
    for _ in range(0, dice):
        check = random.random()*100
        if check > 50:
            successes += 1
    return successes


def normal_damage(base_damage, attack_stat, defense_stat, bonus_attack, bonus_defense):
    raw_power = base_damage + attack_stat + bonus_attack
    raw_defense = defense_stat + bonus_defense
    damage = raw_power - raw_defense
    if damage < 1:
        damage = 1
    return damage
