import sys
import os
import json
import time

from IPython.core.display import clear_output

from GAME_CORE.account import Account
from GAME_CORE.battle import Battle
from GAME_CORE.mob import Mob


# the Menu system
class Menu:

    def __init__(self):
        # current training ground session
        self.battle = None
        self.mob = None  # mob in current training ground
        print(f'--- Loading Menu ---')
        f = open(os.getcwd() + "/menu_dict.json")
        self.menu_dict = json.loads(f.read())
        print(f'--- Finished Loading menu DataBase ---')
        self.character = None  # character for current session
        self.account_info = None  # character selection for current session
        self.current_menu = 'manage_account'  # track which interface user is at
        self.account = Account()  # Account class for current selection
        # self.account_df = self.account.account_df

    def manage_account_menu(self):
        flag = True
        while flag:
            alter = input('Do you want to create/delete account? Y/N ')
            if alter == 'Y':
                # Y for register N for deletion
                register = input('Register? Y/N ')
                if register == 'Y':
                    # ask for account
                    account = input("Enter your account: ")
                    # ask for password
                    password = input("Enter your password (no space please): ")
                    self.account.create_new_account(account, password)
                # if deletion
                elif register == 'N':
                    # ask for account
                    account = input("Enter your account: ")
                    # ask for password
                    password = input("Enter your password: ")
                    self.account.delete_account(account, password)
                else:
                    print('>>> Please enter "Y" or "N" <<<')
                flag = False
            elif alter == 'N':
                flag = False
                pass
            else:
                print('>>> Please enter "Y" or "N" <<<')

    def login_menu(self):
        '''
        log in with user input
        :return:
        '''
        if self.account.is_logged_in:
            print(f'>>> {self.account.account} is currently logged in <<<')
            logout = input(f'Do you want to logout? Y/N ')
            if logout == 'Y':
                self.account.logout()
                print('>>> Proceeding to manage_account <<<')
                self.current_menu = 'manage_account'
            elif logout == 'N':
                pass
            else:
                print('>>> Please enter "Y" or "N" <<<')
        else:
            while not self.account.is_logged_in:
                try:
                    # ask for account
                    account = input("Enter your account: ")
                    # ask for password
                    password = input("Enter your password: ")
                    # flag credential to be True if correct combination
                    self.account.login(account, password)
                    if not self.account.is_logged_in:
                        raise AssertionError
                except (KeyError, AssertionError):
                    print(f'>>> Wrong Combination Of Credentials <<<')

            pass

    def character_menu(self):
        character_selected = False
        # load account info
        print(f'--- Loading {self.account.account} Info ---')
        self.account_info = self.account.load_account_info()
        print(f'--- Finished Loading {self.account.account} Info ---')
        # if no character in selection menu
        if self.account.account_info.shape[1] < 1:
            print(f'>>> {self.account.account} currently has no character <<<')
            # ask name to create new character
            character_name = input("Enter your first character's name: ")
            # create new character
            self.account.create_new_character(character_name)
            # load account info
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
                self.character.display_stats()
                character_selected = True
            except (AttributeError, KeyError):
                pass
                # print('>>> That Character Does Not Exist <<<')
            except ValueError:
                print(f'>>> Please Enter A Number <<<')
        # toggle next menu
        self.current_menu = 'in_game'

    def in_game_menu(self):
        # TODO: in_game menu
        pass

    def training_ground_menu(self):
        clear_output(wait=True)
        # TODO: class map
        # map.display_map()
        invalid_map = True
        while invalid_map:
            try:
                map_id = int(input('Which map do you want to go: '))
                self.mob = Mob()
                invalid_map = False
            except NameError:
                print(f'>>> {map_id} is not an option <<<')
        self.battle = Battle(self.character, self.mob, map_id)
        time.sleep(0.5)
        self.battle.battle_ground()
        time.sleep(0.5)
        self.battle.battle_summary()

    def next_menu(self):
        # clear_output(wait=True)
        invalid_next = True
        while invalid_next:
            print(f'\n>>> You are currently @ {self.current_menu} <<<')
            for key, value in zip(self.menu_dict[self.current_menu], self.menu_dict[self.current_menu].values()):
                print(f'{key}: {value}')
            next_menu = input(f'Where do you want to proceed next: ')
            try:
                self.current_menu = self.menu_dict[self.current_menu][next_menu]
                print(f'--- Proceeding to {self.current_menu} ---')
                invalid_next = False
            except KeyError:
                print(f'>>> {next_menu} is not an option <<<')

    def menu(self):
        '''
        All interfaces (connected interfaces) included:
        login (character selection, TODO: account creation)
        character_selection (login, character_creation/deletion, in_game)
        TODO: in_game
        '''
        if self.current_menu == 'manage_account':
            self.manage_account_menu()
        elif self.current_menu == 'login':
            self.login_menu()
        elif self.current_menu == 'character_selection':
            self.character_menu()
        elif self.current_menu == 'in_game':
            self.in_game_menu()
        elif self.current_menu == 'training_ground':
            self.training_ground_menu()
        else:
            print(f'--- Quiting Toxic Shroom Game ---')
            self.account.save_progress()
            sys.exit()
        self.next_menu()

    def start(self):
        '''
        Actual game play
        :return:
        '''
        game = True
        self.current_menu = 'manage_account'
        while game:
            self.menu()
