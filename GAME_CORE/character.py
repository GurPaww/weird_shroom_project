from datetime import date
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


class Character:

    def __init__(self, level=1, experience=0, job_id=0, character_name='Noob 516', str_=10, dex=4, luk=4, int_=4,
                 stat_point=0, ability_point=0):
        """
        str level: level of the character
        str experience_pct: character's raw experience_pct amount at current level
        str job_id: job ID of the character
        str character_name: name of the character
        str str_:
        str dex:
        str luk:
        str int_:
        str stat_point: unassigned stat points from leveling up
        str ability_point: unassigned ability points from leveling up or job advancing
        """
        print(f'--- Loading Job Info ---')
        f = open(os.getcwd() + "/JOB_INFO/job_dict.json")
        job_dict = json.loads(f.read())
        self.job_df = pd.DataFrame(job_dict)
        self.job_df.columns = map(int, list(self.job_df.columns))
        print(f'--- Finished Loading Job Info ---')
        print(f'--- Loading Exp Info ---')
        # note iloc[12,] gives info on level 13, i.e. exp amount needed to lvl 14
        self.exp_df = pd.read_csv(f'EXP_INFO/exp_chart.csv', index_col=0)
        print(f'--- Finished Loading Exp Info ---')
        self.level = int(level)
        # level needs to be greater than 0
        assert self.level > 0
        self.exp = int(experience)
        # experience_pct to 2 digits after decimal
        self.exp_pct = round(100 * int(experience) / self.exp_df.iloc[self.level - 1, 0], 2)
        self.job_id = int(job_id)
        self.character_name = character_name
        # convert to corresponding job name based on job id
        self.job_name = self.job_df[self.job_id]['job_name'].capitalize()
        self.str_ = int(str_)
        self.dex = int(dex)
        self.luk = int(luk)
        self.int_ = int(int_)
        # only magician class job is magic attack
        self.attack_type = 'matt' if self.job_df[self.job_id]['job_class'] == 'magician' else 'watt'
        # generally beginner, warrior, and pirate main stat is str, dex for archer, luk for thief, int for magician
        main_stat = self.job_df[self.job_id]['main_stat']
        # weapon attack should be based on different main stat
        if main_stat == 'str':
            self.weapon_attack = self.str_ * 1  # times weapon factor - from weapon
        elif main_stat == 'dex':
            self.weapon_attack = self.dex * 1
        elif main_stat == 'luk':
            self.weapon_attack = self.luk * 1
        # TODO: a separated function to load based on equipment and skills
        # All below attribute will be impacted by equipments and skills
        # magic attack only based on int
        self.magic_attack = self.int_ * 1  # magic factor - from weapon
        # weapon defense
        self.weapon_defence = 10
        # magic defense
        self.magic_defence = 5
        # current HP
        self.hit_point = self.level * 10 + self.str_ * 5
        # max HP
        self.max_hit_point = self.level * 10 + self.str_ * 5
        # excess accuracy - can nullify mobs' evasion chance
        self.accuracy = (0.0006 * self.dex) / (1 + 0.0006 * self.dex)
        # have chance to evade a mob's attack, displayed "~Miss~"
        self.evasion = (0.0006 * self.luk) / (1 + 0.0006 * self.luk)
        # current MP
        self.mana_point = self.level * 8 + self.int_ * 5
        # max MP
        self.max_mana_point = self.level * 8 + self.int_ * 5
        # stat point
        self.stat_point = int(stat_point)
        # skill point
        self.ability_point = int(ability_point)



    def display_info(self):
        # level and job
        print(f'\nLvl: {self.level} {self.job_name}')
        # HP bar
        print(
            f'[{"".join(["/"] * (self.hit_point*20//self.max_hit_point))}'
            f'{"".join([" "] * (20 - self.hit_point*20//self.max_hit_point))}]  '
            f'{self.hit_point} / {self.max_hit_point} {round(self.hit_point/self.max_hit_point,2)*100} %')
        # MP bar
        print(
            f'[{"".join(["/"] * (self.mana_point * 20 // self.max_mana_point))}'
            f'{"".join([" "] * (20 - self.mana_point * 20 // self.max_mana_point))}]  '
            f'{self.mana_point} / {self.max_mana_point} {round(self.mana_point / self.max_mana_point, 2) * 100} %')
        # exp bar
        print(
            f'[{"".join(["="] * (int(self.exp_pct) // 5))}{"".join([" "] * (20 - int(self.exp_pct) // 5))}]  '
            f'{self.exp_pct} %')
        print(f'{self.character_name}')

    def display_stats(self):
        print(f'\nStr: {self.str_}\nDex: {self.dex}\nLuk: {self.luk}\nInt: {self.int_}')
        print(f'Weapon Attack: {self.weapon_attack}\nMagic Attack: {self.magic_attack}\n'
              f'Accuracy: {round((1 + self.accuracy) * 100, 2)} %\nEvasion: {round(self.evasion * 100, 2)} %')

    # TODO: display skill

    def issue_attack(self):
        if self.attack_type == 'watt':
            return self.weapon_attack, self.accuracy, self.attack_type
        elif self.attack_type == 'matt':
            return self.magic_attack, self.accuracy, self.attack_type

    # TODO: issue_spell
    def receive_attack(self, incoming_damage, attack_type):
        # damage
        if attack_type == 'watt':
            damage = incoming_damage - self.weapon_defence
        else:
            damage = incoming_damage - self.magic_defence
        damage = max(damage, 1)
        # check if evade
        if np.random.rand() * 100 <= self.evasion:
            damage = 0
            print(f'~ MISS ~')
        else:
            print(f'~ {damage} ~')
        self.hit_point -= damage
        # minimum hp is 0
        self.hit_point = max(self.hit_point, 0)
        self.display_info()

    def kill_monster(self, exp_amount):
        self.exp += exp_amount
        self.check_if_lvl_up()

    def finish_quest(self, exp_amount):
        self.exp += exp_amount
        self.check_if_lvl_up()

    def is_dead(self):
        if self.hit_point <= 0:
            # drop 10% experience_pct if dead / minus 5 because this function is called twice.
            self.exp_pct -= 5
            self.exp = int(self.exp_df.iloc[self.level-1, 0])
            # TODO: if beginner class then don't drop / if luk is high then drop less
            return True
        else:
            return False

    def lvl_up(self):
        self.level += 1
        # TODO: cygnus knight + 6 sp from leveling up
        self.stat_point += 5
        self.ability_point += 3
        self.exp -= self.exp - self.exp_df.iloc[self.level-2, 0]
        self.exp_pct = round(100 * int(self.exp) / self.exp_df.iloc[self.level - 1, 0], 2)
        self.display_info()

    def check_if_lvl_up(self):
        self.exp_pct = round(100 * int(self.exp) / self.exp_df.iloc[self.level - 1, 0], 2)
        # if accumulative enough exp to next level
        if self.exp_pct >= 100:
            self.lvl_up()
        else:
            pass
        self.display_info()

    def job_advancement(self, advance, job_id):
        # TODO: stat check beside level check
        # add one if success advancement
        self.ability_point += 1
        if advance == 1 and self.level >= 10:
            self.job_id = job_id
            log = f'|Successfully advanced to {self.job_df[job_id]["job_name"].capitalize()}|'
            print(f'{"".join(["-"]*(len(log)))}')
            print(f'{log}')
            print(f'{"".join(["-"] * (len(log)))}')
            self.display_info()
        elif advance == 2 and self.level >= 30:
            self.job_id = job_id
            log = f'|Successfully advanced to {self.job_df[job_id]["job_name"].capitalize()}|'
            print(f'{"".join(["-"] * (len(log)))}')
            print(f'{log}')
            print(f'{"".join(["-"] * (len(log)))}')
            self.display_info()
        else:
            # remove the add one if advancement requirement not satisfied.
            self.ability_point -= 1
            print(f'Do not meet requirement to advance to {self.job_df[job_id]["job_name"].capitalize()}')

    # TODO: inventory
    # TODO: sp assign
    # TODO: ap assign