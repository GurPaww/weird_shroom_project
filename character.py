from datetime import date
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import pickle
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


class Character:

    def __init__(self, level=1, experience=0, job_id=0, character_name='Noob 516'):
        '''
        int level: level of the character
        int experience: percentage of the character at current level
        int job_id: job ID of the character
        str character_name: name of the character
        '''
        print(f'--- Loading Job Info ---')
        f = open(os.getcwd() + "/job_dict.json")
        job_dict = json.loads(f.read())
        self.job_df = pd.DataFrame(job_dict)
        print(f'--- Finished Loading Job Info ---')
        self.level = int(level)
        self.experience = int(experience)
        self.job_id = job_id
        self.character_name = character_name
        self.job_name = self.job_df[self.job_id]['job_name'].capitalize()

    def display_info(self):
        print(f'Lvl: {self.level} {self.job_name}')
        # exp bar
        print(f'[{"".join(["="] * (self.experience // 5))}]  {self.experience} %')
        print(f'{self.character_name}')

    def kill_monster(self, exp_amount):
        self.experience += exp_amount

    def finish_quest(self, exp_amount):
        self.experience += exp_amount

    def dead(self):
        self.experience -= 10

    def check_if_lvl_up(self):
        if self.experience >= 100:
            self.experience -= 100
            self.level += 1
        else:
            pass

    def job_advancement(self, advance, job_id):
        # TODO: stat check beside level check
        if advance == 1 and self.level >= 10:
            self.job_id = job_id
        elif advance == 2 and self.level >= 30:
            self.job_id = job_id
        else:
            print(f'Do not meet requirement to advance to {job_id}')

    # TODO: inventory
