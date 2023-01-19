import os
import json
import time
from GAME_CORE.menu import Menu


class GamePlay:

    def __init__(self):
        print(f'--- Initializing Toxic Shroom Game ---')
        f = open(os.getcwd() + "/CONFIG/configuration.json")
        config_dict = json.loads(f.read())
        self.start_time = time.ctime(time.time())
        self.version = config_dict['GameVersion']
        self.menu = Menu()
        print(f'--- Game Is Loaded @ V{self.version} ---\n--- Current Time Is {self.start_time} ---')

    def start(self):
        self.menu.start()
