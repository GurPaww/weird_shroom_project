import os
import json
import pandas as pd
import warnings
from GAME_CORE.character import Character

warnings.simplefilter(action='ignore', category=FutureWarning)


class Account:
    def __init__(self):
        """
        account_info = character collections, pd.DataFrame
        account = username, str
        is_logged_in = whether an account is logged in or not, bool
        character_id = selected character to proceed to in game
        """
        self.account_info = None
        self.account = None
        self.is_logged_in = False
        self.character_id = None
        print(f'--- Loading Account DataBase ---')
        # account database
        f = open(os.getcwd() + "/ACCOUNT_INFO/account_dict.json")
        account_dict = json.loads(f.read())
        self.account_df = pd.DataFrame(account_dict)
        # account ID for registration
        f = open(os.getcwd() + "/ACCOUNT_INFO/account_id_dict.json")
        self.account_id_dict = json.loads(f.read())
        print(f'--- Finished Loading Account DataBase ---')

    def create_new_account(self, account, password):
        '''

        :param account: username, cannot be redundant to existing accounts
        :param password: password, cannot include space
        :return: Boolean - True creation successful, False otherwise
        '''
        # check if space is in password
        if ' ' in password:
            print(f'>>> {password} contains illegal string <<<')
            return False
        # check if username already in use
        elif account in list(self.account_df.columns):
            print(f'>>> {account} has already been registered <<<')
            return False
        else:
            # get new account ID and update database
            self.account_id_dict['normal'] += 1
            temp = json.dumps(self.account_id_dict)
            f = open(os.getcwd() + "/ACCOUNT_INFO/account_id_dict.json", "w")
            f.write(temp)
            f.close()

            # register new account to database
            self.account_df[account] = [password, 'normal', self.account_id_dict['normal']]
            temp = json.dumps(self.account_df.to_dict())
            f = open(os.getcwd() + "/ACCOUNT_INFO/account_dict.json", "w")
            f.write(temp)
            f.close()

            # new account's account info(empty character template)
            new_account_info = pd.read_csv(f'ACCOUNT_INFO/empty_account.csv', index_col=0)
            new_account_info.to_csv(f'ACCOUNT_INFO/{account}.csv')
            print(f'>>> {account} registered successfully <<<')
            return True

    def delete_account(self, account, password):
        try:
            # compare credential
            assert password == self.account_df[account]['password']
            # confirm with user about deletion
            delete = input(f'Are you sure you want to delete {account}? Y/N ')
            if delete == 'Y':
                # drop corresponding column
                self.account_df.drop(account, axis=1, inplace=True)
                # update database
                temp = json.dumps(self.account_df.to_dict())
                f = open(os.getcwd() + "/ACCOUNT_INFO/account_dict.json", "w")
                f.write(temp)
                f.close()
                print(f'>>> {account} Has Been Deleted Successfully <<<')
        except (AssertionError, KeyError):
            print(f'>>> Wrong Combination Of Credentials <<<')

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
            # return self.account_info
        else:
            print(f'>>> Please Log In First <<<')

    def create_new_character(self, character_name='Noob 516'):
        if self.account_info is None:
            print(f'>>> Please Load Account Info First <<<')
        else:
            # shape = the largest index + 1
            character_id = self.account_info.shape[1]
            # level, exp, job_id, name
            self.account_info[character_id] = [1, 0, 0, character_name, 10, 4, 4, 4]
            self.save_progress()

    def select_character(self, character_id):
        if self.account_info is None:
            print(f'>>> Please Load Account Info First <<<')
        else:
            try:
                info = self.account_info[character_id]
                self.character_id = character_id
                return Character(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7])
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
                    self.save_progress()
                except KeyError:
                    print('>>> That Character Does Not Exist <<<')

    def save_progress(self):
        if self.account_info is None:
            print(f'>>> Please Load Account Info First <<<')
        else:
            # self.account_info = new_account_info
            print(f'--- Saving Current Account Progress ---')
            self.account_info.to_csv(f'ACCOUNT_INFO/{self.account}.csv')
