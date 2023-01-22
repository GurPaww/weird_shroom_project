from datetime import date
import time
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import warnings
from GAME_CORE.character import Character
from GAME_CORE.mob import Mob

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
        # TODO: map dictionary
        self.map = 'Port Road: Six Path Crossway'
        print(f'--- Arrived Battle Ground @ {self.map} ---')
        # whether to take/continue the fight or not
        self.fight = None

    def battle_preparation(self):
        # if self.fight is None it means no attacks have taken place yet
        if self.fight is None:
            # notification of which mob you encounter
            print(f'>>> [{self.mob.name}] Encountered <<<\n')
            # display mob info
            self.mob.display_stats()
            # ask whether to take the fight
            flag = True
            while flag:
                fight = input(f'Do you want to take the fight with [{self.mob.name}]? Y/N ')
                if fight == 'Y' or fight == 'N':
                    self.fight = fight
                    flag = False
                else:
                    print('>>> Please enter "Y" or "N" <<<')
        # if self.fight = 'Y'
        elif self.fight == 'Y':
            flag = True
            while flag:
                fight = input(f'Continue fighting with [{self.mob.name}]? Y/N ')
                if fight == 'Y' or fight == 'N':
                    self.fight = fight
                    flag = False
                else:
                    print('>>> Please enter "Y" or "N" <<<')
        # no circumstance for self.fight = 'N' to pass in here
        else:
            print('System: I do not see a fight here...')


    # in-combat analysis
    """
    Player controlled character and spawned mob will take a fight, where they attack in turns.
    Player always attacks first (issue attack), and mob always receives attack first.
    """
    def battle_ground(self):
        # if no decision is detected for whether to fight or not
        if self.fight is None:
            self.battle_preparation()

        # player attack first
        turn = 'character'
        # while both alive
        while self.fight == 'Y':
            time.sleep(0.5)
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
            # if one side dies
            if self.character.is_dead() or self.mob.is_dead():
                break
            self.battle_preparation()

    # Battle summary
    def battle_summary(self):
        print(f'\n--- Loading Post-Battle Summary ---')
        # if player survive
        if self.mob.is_dead():
            # TODO: mob exp chart based on level and read from dataframe
            # reward exp based on mob's level
            exp_gain = round(np.power(self.mob.level, 1.3))
            # Idea: build exp and loot notification function in mob class
            print(f'System: Gained {exp_gain} Exp')
            # TODO: loot list
            print(f'System: Looted:\n59 Mesos\n1 Orange Mushroom Cap')
            self.character.kill_monster(exp_gain)
        elif self.character.is_dead():
            # same for character
            # Randomize creative death notification, like minecraft
            print(f'System: {self.character.character_name} Got Killed ')
            print(f'>>> Teleporting Back To Nearest Town <<<')
            # hp becomes 50 after reviving
            self.character.hit_point = 50
            self.character.display_info()
        else:
            print(f'>>> Battle Not Finished Yet <<<')
        self.fight = None







