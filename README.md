# weird_shroom_project

This is a (hardly) a buget replica of MMORPG [Maplestoli](https://maplestory.nexon.net/landing).

Please run demo.ipynb for demonstration.

## Intro to different menu
### 1. Manage Account
This is where you can register or delete accounts. To register an account, you need to provide a username that is different from any of the registered account stored in database, and a password that does not include white space. To delete an account, you need to supply an existing pair of credentials stored in database. The game will ask you for confirmation on deleting account once more.

If you want to proceed with an existing account, just say "N" to the first prompt.

### 2. Login
Just like deleting an account, you need to provided an existing pair of credential stored in database.

The login status will be remembered until you confirm to logout in Login menu again, even if you re-load the game (without restarting the kernel).

### 3. Character Selection
This is where you can view your created chracter and select from the collection. If the collection is empty, you will be automatically prompt to create you first character, with a character name. _For account that has a character, Character Creation and Deletion in-progress._

_All descriptions below still in-progress_
### 4. In Game
This is the main interface. You can go training to level up your character and farm for mesos [ˈmoʊzəs] -- don't worry if you didn't get this pronunciation reference. Some other options include hene-hoeing.

### 5. Training Ground
This is the battle field of your character and mobs. Currently map and mob are hard coded, while the exp and loot rewards are not updated with your character. Just to showcase the idea.

### 6. Hene-hoe
Nothing done here.

## Some basis of shroom game
### 1. Four stats - strength (str), dexterity (dex), luck (luk), intelligence (int)
Each job has a main stat. 
Warrior class uses str;
Archer -- dex;
Thief -- luk;
Magician -- int;
Pirate -- str.

### 2. Job advancement
TBA

## Some other concepts in progress
### a) Equipment
Equipment system should boost your character's various stats, such as weapon/magic attack and defense.

### b) Spells
Active spells -- can be power attack or buff / cost mana

Passive spells -- can boost stats, such as evasion / doesn't cost mana

## ...TO BE CONTINUED...
