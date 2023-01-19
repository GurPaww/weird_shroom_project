from datetime import date
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


class Mob:

    def __init__(self, name='Orange Mushroom', level=8, weapon_defence=10, weapon_attack=20, magic_defence=2,
                 magic_attack=2, hit_point=60, mana_point=5, evasion=1, attack_type='watt', skill=None, drops=None):
        """
        :param name: str
        :param level: int
        :param weapon_defence: int
        :param weapon_attack: int
        :param magic_defence: int
        :param magic_attack: int
        :param hit_point: HP, int
        :param mana_point: MP, int
        :param evasion: int
        :param attack_type: 'watt' = weapon attack, 'matt' = magic attack
        :param skill: array
        :param drops: array
        """
        self.name = name
        self.level = level
        self.weapon_defence = weapon_defence
        self.weapon_attack = weapon_attack
        self.magic_defence = magic_defence
        self.magic_attack = magic_attack
        self.hit_point = hit_point
        self.mana_point = mana_point
        self.max_hit_point = hit_point
        self.max_mana_point = mana_point
        self.evasion = (0.006 * evasion) / (1 + 0.006 * evasion)
        self.attack_type = attack_type
        # self.skill
        # self.drop

    def display_info(self):
        # level and name
        print(f'\nLevel: {self.level} {self.name}\n')
        # HP bar
        print(
            f'[{"".join(["/"] * (self.hit_point * 20 // self.max_hit_point))}'
            f'{"".join([" "] * (20 - self.hit_point * 20 // self.max_hit_point))}]  '
            f'{self.hit_point} / {self.max_hit_point} {round(self.hit_point / self.max_hit_point, 2) * 100} %')
        # MP bar
        print(
            f'[{"".join(["/"] * (self.mana_point * 20 // self.max_mana_point))}'
            f'{"".join([" "] * (20 - self.mana_point * 20 // self.max_mana_point))}]  '
            f'{self.mana_point} / {self.max_mana_point} {round(self.mana_point / self.max_mana_point, 2) * 100} %')

    def display_stats(self):
        print(f'Weapon Attack: {self.weapon_attack}\nMagic Attack: {self.magic_attack}\n'
              f'Evasion: {round(self.evasion * 100, 2)} %\nAttack Type: {self.attack_type}')

    def issue_attack(self):
        if self.attack_type == 'watt':
            return self.weapon_attack, self.attack_type
        elif self.attack_type == 'matt':
            return self.magic_attack, self.attack_type
        else:
            print('>>> Invalid Attack Type <<<')

    def receive_attack(self, incoming_damage, accuracy, attack_type):
        # damage
        if attack_type == 'watt':
            damage = incoming_damage - self.weapon_defence
        else:
            damage = incoming_damage - self.magic_defence
        damage = max(damage, 1)

        if np.random.rand() * 100 <= (self.evasion-accuracy):
            damage = 0
            print(f'~ MISS ~')
        else:
            print(f'~ {damage} ~')
        self.hit_point -= damage
        self.display_info()

    def is_dead(self):
        if self.hit_point <= 0:
            return True
        else:
            return False
