import texttable as tt
from random import randrange as rrange
# from command_demo08 import GameMain
from name_creator_elf import namebuilder
# from libs.commands import GameCommLib
from libs.utils import GameUtils


class GamePlayer(GameUtils):

    def __init__(self):
        # GameCommLib.__init__(self)

        self.eq_armor_slots = {'head':    {'name':'','DEF':1,'OFF':0,'ATT':0,'equips':'head','mod':-1},
                               'body':   {'name':'','DEF':3,'OFF':0,'ATT':0,'equips':'body','mod':0},
                               'legs': {'name':'','DEF':1,'OFF':0,'ATT':0,'equips':'legs','mod':0},
                               'lhand':  {'name':'','DEF':1,'OFF':0,'ATT':0,'equips':'left hand','mod':0},
                               'rhand':   {'name':'','DEF':1,'OFF':1,'ATT':1,'equips':'right hand','mod':+1}}

        self.STR = rrange(6,20)
        self.DEX = rrange(6,20)
        self.CON = rrange(6,20)
        self.stats = [self.STR, self.DEX, self.CON]

        self.run = False

    def player_command(self, equip_data, player_name="default"):
        # player command #
        """
            lists player info and stats use "stats" to access
        """

        self.tab = tt.Texttable()
        self.header = ['PART', 'EQUIPPED', 'DEF', 'OFF', 'ATT', 'MOD']
        self.equipment_list = []
        self.row = []
        if equip_data:
            equip_item = equip_data[0][0]
            equip_location = equip_data[0][1]
            print('Player Command', equip_item, equip_location)
            if equip_location[1] in self.eq_armor_slots.keys():
               self.eq_armor_slots[equip_location[1]]['name'] = equip_item[1]
            for each in self.eq_armor_slots.values():
                print(']]', each)

        print('')
        print('Name: {} '.format(player_name))
        print('')
        print('-'*50)
        print('## STATS ##')
        print('-'*50)
        print('\tSTR - {}'.format(self.stats[0]))
        print('\tDEX - {}'.format(self.stats[1]))
        print('\tCON - {}'.format(self.stats[2]))
        print('-'*50)
        self.tab.header(self.header)
        for each in sorted(self.eq_armor_slots.keys()):
                self.row = [self.eq_armor_slots[each]['equips'],
                       self.eq_armor_slots[each]['name'],
                       self.eq_armor_slots[each]['DEF'],
                       self.eq_armor_slots[each]['OFF'],
                       self.eq_armor_slots[each]['ATT'],
                       self.eq_armor_slots[each]['mod']]
                self.tab.add_row(self.row)

        self.equipment_list = self.tab.draw()

        print(self.equipment_list)
        self.row = []

        print('_'*50)

        # else:
        #     print('\nNothing equipped..')
        # print('-'*50)
        print('\n\n')
        input('<continue>')
        self.clr_screen(30)
        return
