from random import randrange as rrange
from random import choice
#from command_demo08 import GameMain
#from libs.commands import *
#from libs.items import *
from libs.utils import GameUtils

class GameCreatures(GameUtils):

    def __init__(self):
        GameUtils.__init__(self)

        self.creatures = {'rat':
                              {'name': 'rat',
                               'freq': 70,
                               'att': 1},
                          'wolf':
                              {'name': 'wolf',
                               'freq': 35,
                               'att': 2},
                          'spider':
                              {'name': 'small spider',
                               'freq': 50,
                               'att': 2},
                          'dragon':
                              {'name': 'dragon',
                               'freq': 10,
                               'att': 30},
                          }

        self.creature_pops = [
                                'A {} skitters about the room..',
                                'A {} runs under foot.',
                                'Without warning a {} growls at you.',
                                'A {} bares its teeth at you.',
                              ]

        self.rooms_creatures = {}

    def creature_appearance(self, num=1, rooms=None, room_temp=None):
        """
            Roll for creature,
            uses DB info of creature frequency
        """
        self.creature_select = choice(list(self.creatures.keys()))
        self.creature_does = choice(self.creature_pops)

        for each in range(num):
            rolled = self.die_roll()
            # appearance rolls
            # print('DIE ROLL = {}'.format(rolled))
            # print('CREATURE = {}'.format(self.creatures[self.creature_select]))
            # print('ROOMS CREATURES BEFORE: {}'.format(self.rooms_creatures))
            room_ = rooms[room_temp['room']][0]

            if self.creatures[self.creature_select]['freq'] >= rolled\
                    and room_ not in list(self.rooms_creatures.keys()):

                # print('DEBUG::{}: is appearing, roll was {}:{}'.format(self.creatures[self.creature_select]['name'],
                # rolled,
                # self.creatures[self.creature_select]['freq']))
                # print('ROOMS TEMP', rooms[room_temp['room']][0])
                # if rooms[room_temp['room']][0] not in list(self.rooms_creatures.keys()):

                """
                    If no creature is present add this creature to this room...
                """

                self.rooms_creatures[room_] = self.creatures[self.creature_select]
                # print('ROOMS CREATURES AFTER: {}'.format(self.rooms_creatures))
                return self.rooms_creatures, True, self.creature_does

            elif self.creatures[self.creature_select]['freq'] >= rolled\
                    and room_ in list(self.rooms_creatures.keys()):

                # print('DEBUG::{}: is not appearing, roll was {}:{}'.
                #   format(self.creatures[self.creature_select]['name'],
                # rolled,
                # self.creatures[self.creature_select]['freq']))
                """
                    Creature already here, don't add another
                """
                return self.rooms_creatures, False, self.creature_does

            else:
                # print('>>Nothing happened, no creatures match criteria<<')
                return 0, False
