from datetime import date
import time
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
from GAME_CORE.character import Character
from mob import Mob

warnings.simplefilter(action='ignore', category=FutureWarning)


class Battle:

    def __init__(self, character, mob, map_id=1):
        # make sure we passed in one character (player) and one mob (monster)
        try:
            assert isinstance(character, Character)
            assert isinstance(mob, Mob)

        except AssertionError:
            print('>>> Invalid Battle <<<')
        self.character = character
        self.mob = mob
        self.map = 'Port Road: Six Path Crossway'
        print(f'--- Arrived Battle Ground @ {self.map} ---')

    def battle_ground(self):
        # player attack first
        turn = 'character'
        print(f'>>> [{self.character.character_name}] Encounters [{self.mob.name}] <<<\n')
        self.mob.display_stats()
        # while both alive
        while not self.character.is_dead() and not self.mob.is_dead():
            time.sleep(1)
            if turn == 'character':
                print(f'\n\nSystem: [{self.character.character_name}] Attacks')
                att, acc, type_ = self.character.issue_attack()
                self.mob.receive_attack(att, acc, type_)
                turn = 'mob'
            elif turn == 'mob':
                print(f'\n\nSystem: [{self.mob.name}] Attacks')
                att, acc, type_ = self.character.issue_attack()
                self.character.receive_attack(att, acc)
                turn = 'character'

    # Battle summary
    def battle_summary(self):
        print(f'\n--- Loading Post-Battle Summary ---')
        # if player survive
        if self.mob.is_dead():
            # TODO: self.mob.exp()
            # Idea: build exp and loot notification function in mob class
            print(f'System: Gained 100 Exp')
            print(f'System: Looted:\n59 Mesos\n1 Orange Mushroom Cap')
            self.character.display_info()
        elif self.character.is_dead():
            # same for character
            # Randomize creative death notification, like minecraft
            print(f'System: {self.character.character_name} Got Killed ')
            print(f'>>> Teleporting Back To Nearest Town <<<')
            self.character.display_info()
        else:
            print(f'>>> Battle Not Finished Yet <<<')







