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
from account import Account


class GamePlay:

    def __init__(self):
        '''

        '''
        self.character = None # character for current session
        self.account_info = None # character selection for current session
        self.account = None # Account class for current selection
        self.current_menu = 'login' # track which interface user is at
        print(f'--- Loading Account DataBase ---')
        f = open(os.getcwd() + "/account_dict.json")
        account_dict = json.loads(f.read())
        self.account_df = pd.DataFrame(account_dict)
        print(f'--- Finished Loading Job DataBase ---')

    def login_menu(self):
        '''
        log in with user input
        :return:
        '''
        # TODO: account creation
        credential = False
        while not credential:
            try:
                # ask for account
                account = input("Enter your account: ")
                # ask for password
                password = input("Enter your password: ")
                # create class Account to verify with database
                self.account = Account(self.account_df)
                # AssertionError will be raise if credential is wrong
                self.account.login(account, password)
                # flag credential to be True if correct combination
                credential = True
                # load account info (characters)
                print(f'--- Loading {self.account.account} Info ---')
                self.account_info = self.account.load_account_info()
                print(f'--- Finished Loading {self.account.account} Info ---')
            except KeyError or AssertionError:
                print(f'>>> Wrong Combination Of Credentials <<<')
        # toggle next menu
        self.current_menu = 'character_selection'
        pass

    def character_menu(self):
        character_selected = False
        # if no character in selection menu
        if self.account_info.shape[1] < 1:
            # ask name to create new character
            character_name = input("Enter character name: ")
            # create new character
            self.account.create_new_character(character_name)
            # reload account info
            print(f'--- Reloading {self.account.account} Info ---')
            self.account_info = self.account.load_account_info()
            print(f'--- Finished Reloading {self.account.account} Info ---')

        # TODO: menu to create more character and delete character @ selection

        # character selection
        while not character_selected:
            try:
                # enter character ID to select character
                character_id = input("Enter character ID: ")
                self.character = self.account.select_character(int(character_id))
                self.character.display_info()
                character_selected = True
            except AttributeError or KeyError:
                pass
                # print('>>> That Character Does Not Exist <<<')
            except ValueError:
                print(f'>>> Please Enter A Number <<<')
        # toggle next menu
        self.current_menu = 'in_game'

    def in_game_menu(self):
        # TODO: in_game menu

        # toggle next menu
        self.current_menu = 'quit'

    def menu(self):
        '''
        All interfaces (connected interfaces) included:
        login (character selection, TODO: account creation)
        character_selection (login, character_creation/deletion, in_game)
        TODO: in_game
        '''
        if self.current_menu == 'login':
            self.login_menu()
        elif self.current_menu == 'character_selection':
            self.character_menu()
        elif self.current_menu == 'in_game':
            self.in_game_menu()
        else:
            print(f'--- Quiting Toxic Shroom Game ---')
            quit()

    def start(self):
        '''
        Actual game play
        :return:
        '''
        game = True
        while game:
            self.menu()


