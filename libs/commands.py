from __future__ import print_function
from name_creator_elf import namebuilder
import sqlite3
from random import randrange as rrange
import texttable as tt
from libs.items import *
from libs.player import GamePlayer


#############################################################
# class comm_lib                                            #
#               class library for commands used in          #
#               text based game engine.                     #
#                                                           #
#                                                           #
#                                                           #
#                                                           #
#############################################################

class GameCommLib(GameItems, GamePlayer):

    def __init__(self):
        GameItems.__init__(self)
        GamePlayer.__init__(self)

        self.connect_db = sqlite3.connect('SQL_COMMAND_DEMO.db')
        self.conn = self.connect_db.cursor()
        self.exam = self.conn.execute("SELECT * FROM 'room_objects'")
        self.stored_objects_data = sorted(self.exam.fetchall())
        self.commands_proc = {'search':          self.search_command,
                              'get':             self.get_command,
                              'drop':            self.drop_command,
                              'inventory':       self.inventory_command,
                              'help':            self.help_command,
                              'look':            self.look_command,
                              'stats':           self.player_command,
                              'player':          self.player_command,
                              'equip':           self.equip_command,
                              'attack':          0,
                              'examine':         self.examine_command,
                              }

        self.room_temp = {'room': 104, 'row': 2, 'column': 2}
        self.list_items = GameItems()
        self.gold = []
        self.player_name = namebuilder(3, 9)
        self.last_name = namebuilder(5, 8)
        """ will be assigned to DB later """
        self.can_be_equipped = {
                          'FF1': {'name': 'helm',
                                  'type': 'head'},
                          'FF2': {'name': 'buckler',
                                  'type': 'lhand'},
                          'FF3': {'name': 'knife',
                                  'type': 'rhand'},
                          'FF4': {'name': 'stick',
                                  'type': 'rhand'},
                          'FF5': {'name': 'cotton shirt',
                                  'type': 'body'},
                          'FF6': {'name': 'leather leggings',
                                  'type': 'legs'},
                          'FF7': {'name': 'cloth hat',
                                  'type': 'head'}
                          }

        self.equipped = []
        self.equipped_on_player = []
        self.STR = mt.ceil(rnd.randrange(6,20))
        self.DEX = mt.ceil(rnd.randrange(6,20))
        self.CON = mt.ceil(rnd.randrange(6,20))
        self.stats = [self.STR, self.DEX, self.CON]
        self.area = [
                 ['#','#','#','#'],
                 ['#',101,102,'#'],
                 ['#',103,104,'#'],
                 ['#',105,'#','#'],
                 ['#','#','#','#']


                ]
        self.backpack = ['knife','buckler','cloth hat','knife','cotton shirt']

    # look command #
    """
        Shows Player room surroundings again, also reflects any changes in room.
        currently just shows self.area data...
    """
    def look_command(self):
        print('')
        print('\tlooking around you see:')
        if len(self.area) > 0:
            for things in self.area:
                print('\t{},'.format(things), end='')
            print('')
        else:
            print('\tYou see a lot of dirt, nothing else just dirt!')
        return

    # inventory command #
    """
        Shows inventory in players backpack as well as equipped items currently on player
    """
    def inventory_command(self):
        x = 0
        print('')
        print('\t<<<<<<BACKPACK>>>>>')
        print('')
        if len(self.backpack) > 0:
            print('')
            for item in self.backpack:
                x += 1
                if item in self.equipped:
                    print('\t*{:5} --- {}'.format(x, item))
                else:
                    print('\t{:5} --- {}'.format(x, item))
            print('\tyou are carrying {}gp in coins'.format(sum(self.gold)))
        else:
            print('\tThere is nothing in your backpack..')
            if sum(self.gold) != 0:

                print('\tyou are carrying {}gp in coins'.format(sum(self.gold)))
            else:
                print('You appear to be quite broke, as you have no money...')
        self.clr_screen(10)

    # search command #
    """
        Searches the room for possible items and gold. Also will reveal secret passages if players
        wisdom is high enough.
    """
    def search_command(self):

        print('you search the area and find...')
        self.random_items(self.room_temp)
        fate = rrange(1,15)
        if fate >= 8:
            coins = rrange(5,25)
            print('\t{} gold coins!'.format(coins))
            self.gold.append(coins)
            print('\tYou have a total of {} gold coins'.format(sum(self.gold)))
            print('')
        else:
            print('Nothing else of importance..')
        return

    # examine command #
    """
        checks objects or items for possible clues or information, may even lead to new objects.

    """
    def examine_command(self, item):

        # is object in inventory or in room ? #
        if item in self.room_items or item in self.rooms[self.room_temp['room']][6] or item in self.backpack:
            for each in self.stored_objects_data:
                #print(each)
                if item in each:
                    self.response(each[2])

        else:
            print('I don\'t see anything like that')

    # get/pickup command #
    """
        pickup objects and place into inventory or hand
    """
    def get_command(self, item):

        #print('ITEM: ',item)
        focus = item
        if self.room_temp['room'] in self.room_items and item in self.room_items[self.room_temp['room']]['items']:
            print('you pick up the {} and place it in your backpack!'.format(focus))
            self.room_items[self.room_temp['room']]['items'].remove(focus)
            self.backpack.append(focus)
            #print('DEBUG### carried value = {}'.format(len(backpack)))
        else:
            print('I don\'t see any {} here...'.format(item))

    # drop command #
    """
        drop objects from inventory or hand
    """
    def drop_command(self, item):

        self.room_items[self.room_temp['room']] = {'items': []}

        #print('ITEM: ',item)
        release = item
        if release in self.backpack or release in self.equipped:
           if release in self.backpack:
               self.backpack.remove(release)
               dropped = True
           if release in self.equipped:
               self.equipped.remove(release)
               dropped = True
           print('You drop the {} on the ground'.format(release))

           self.room_items[self.room_temp['room']]['items'].append(release)

        else:
            print('I don\'t see that item in your inventory.')

    def equip_command(self, item):
        # equip command #
        """
            equip items onto self, only works on equipable items
        """
        if item in self.equipped_on_player:
            print('You are already have a {0} equipped..'.format(item))
            self.main()

        for each in self.can_be_equipped:
            print('>>', self.can_be_equipped[each])
            if self.can_be_equipped[each]['name'] == item and item in self.backpack:
                self.equipped.append(sorted(self.can_be_equipped[each].items()))
                self.equipped_on_player.append(item)
                print('You equip the {}.'.format(item))
                self.main()

        if item in self.room_items[self.room_temp['room']]['items']\
                and item not in self.backpack:
                print('You will have to pick up the {} first..'.format(item))
                self.main()

        else:
            print('You can\'t equip that item')
            self.main()


    # help command #
    """
        list basic commands and basic help --- NEEDS TO BE UPDATED ---
    """

    def help_command(self):
        for command in self.commands.keys():
            print('{}: {}'.format(command, self.commands[command][0]))

    # ## FUNCTION FOR TESTING VALUE OF COMMANDS ##############
    """
        Used for running functions of each command.
    """
    def proccess_commands(self, input_, *args):
        non_standard = ['get', 'drop', 'equip', 'stats', 'player', 'examine']
        if input_ not in non_standard:
            self.commands_proc[input_]()
            self.main()
        elif input_ == "get" or input_ == "drop" or input_ == "equip" or input_ == "examine":
            self.commands_proc[input_](*args)
            self.main()
        elif input_ == "stats" or input_ == "player":
            print('self.equipped', self.equipped)
            self.commands_proc[input_](self.equipped, self.player_name)
            self.equipped = []
            self.main()

