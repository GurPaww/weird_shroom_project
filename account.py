from datetime import date
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import pickle
import warnings
from character import Character

warnings.simplefilter(action='ignore', category=FutureWarning)


class Account:
    def __init__(self, account_df=None):
        '''
        :param account_df: account database
        '''
        self.account_info = None
        self.account = None
        self.is_logged_in = False
        self.character_id = None
        if account_df is None:
            print(f'--- Loading Account DataBase ---')
            f = open(os.getcwd() + "/account_dict.json")
            account_dict = json.loads(f.read())
            self.account_df = pd.DataFrame(account_dict)
            print(f'--- Finished Loading Job DataBase ---')
        else:
            self.account_df = account_df

    def login(self, account, password):
        try:
            assert password == self.account_df[account]['password']
            print(f'>>> Login Successfully <<<')
            self.is_logged_in = True
            self.account = account
        except AssertionError:
            print(f'>>> Wrong Combination Of Credentials <<<')

    def logout(self):
        if not self.is_logged_in:
            print(f'>>> You Are Not Logged In <<<')
        else:
            self.is_logged_in = False
            self.account = None
            print(f'>>> Logout Successfully <<<')

    def load_account_info(self):
        if self.is_logged_in:
            try:
                self.account_info = pd.read_csv(f'ACCOUNT_INFO/{self.account}.csv', index_col=0)
                # convert column names from str to int
                self.account_info.columns = [i for i in range(self.account_info.shape[1])]
                print(self.account_info)
            except NameError:
                print(f'>>> No Character Is Found In The Account <<<')
                self.account_info = pd.read_csv(f'ACCOUNT_INFO/empty_account.csv', index_col=0)
            return self.account_info
        else:
            print(f'>>> Please Log In First <<<')
            pass

    def create_new_character(self, character_name='Noob 516'):
        if self.account_info is None:
            print(f'>>> Please Load Account Info First <<<')
        else:
            character_id = self.account_info.shape[1]
            # level, exp, job_id, name
            self.account_info[character_id] = [1, 0, 0, character_name]
            self.account_info.to_csv(f'ACCOUNT_INFO/{self.account}.csv')

    def select_character(self, character_id):
        if self.account_info is None:
            print(f'>>> Please Load Account Info First <<<')
        else:
            try:
                info = self.account_info[character_id]
                self.character_id = character_id
                return Character(info[0], info[1], info[2], info[3])
            except KeyError:
                print('>>> That Character Does Not Exist <<<')

    def delete_character(self, character_id):
        if self.account_info is None:
            print(f'>>> Please Load Account Info First <<<')
        else:
            confirm = input(f'Deleting {self.account_info[character_id]["character_name"]}? Y/N')
            if confirm == 'Y':
                try:
                    self.account_info.drop(character_id, axis=1, inplace=True)
                    # rearrange character ID
                    self.account_info.columns = [i for i in range(self.account_info.shape[1])]
                    self.account_info.to_csv(f'ACCOUNT_INFO/{self.account}.csv')
                except KeyError:
                    print('>>> That Character Does Not Exist <<<')

    def save_progress(self, new_account_info):
        if self.account_info is None:
            print(f'>>> Please Load Account Info First <<<')
        else:
            self.account_info = new_account_info
            self.account_info.to_csv(f'ACCOUNT_INFO/{self.account}.csv')