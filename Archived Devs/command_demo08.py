from __future__ import print_function
import texttable as tt
from random import choice
from random import randrange as rrange
from name_creator_elf import namebuilder
import sqlite3
import textwrap
from libs.commands import GameCommLib
from libs.items import *
from libs.utils import GameUtils
from libs.player import GamePlayer
from libs.creatures import GameCreatures





class GameMain(GameCommLib, GameCreatures, GamePlayer):

    def __init__(self):
        GameCommLib.__init__(self)
        GameUtils.__init__(self)
        GameItems.__init__(self)
        GamePlayer.__init__(self)
        GameCreatures.__init__(self)

        """
            CONNECT TO DATABASE AND RETRIEVE ROOM DATA
        """

        self.connect_db = sqlite3.connect('SQL_COMMAND_DEMO.db')
        print(self.connect_db)
        self.conn = self.connect_db.cursor()
        self.grab = self.conn.execute("SELECT * FROM 'ROOMS'")
        self.column_name = self.grab.description
        self.stored_rooms_data = sorted(self.grab.fetchall())
        print('Stored Rooms Data == {}'.format(self.stored_rooms_data))

        self.area = [
                 ['#','#','#','#'],
                 ['#',101,102,'#'],
                 ['#',103,104,'#'],
                 ['#',105,'#','#'],
                 ['#','#','#','#']


                ]
        self.room_creat = {}
        self.column = 1
        self.row = 2
        self.times = self.turn()
        self.room_temp = {'room': 104, 'row': 2, 'column': 2}
        #room_coords = [self.row,self.column]

        ## SQLite ROOMS data ##
        self.rooms = {}

        """
            Store each room from database into dict values..
        """

        for each in self.stored_rooms_data:
            self.rooms[each[0]] = each
            # print('Each room stored {},{}'.format(self.rooms[each[0]][0],
            #                                       self.rooms[each[0]]))
        # print('\n',self.rooms)
        self.room_select = choice(list(self.rooms.keys()))
        # print('RS',room_select)
        # print('ROOMS',rooms[room_select])

        #  = {100:{'items':['none']}}
        # = {'room':rooms[room_select][0],'row':rooms[room_select]['row'],'column':rooms[room_select]['column']}

        self.world = """
                    ----------  ---------
                    |  101   |  |  102  |
                    |        \  /       |
                    |       <---->      |
                    |        |  |       |
                    ---|  |---  ---------
                       |  |
                    ---|  |---  ---------
                    |        |  |       |
                    |       <---->      |
                    |        /  \       |
                    |  103   |  |  104  |
                    ---|  |---  ---------
                       |  |
                    ---|  |---
                    |        |
                    |        |
                    |   105  |
                    ----------


        """

        # # DEFINE LISTS #########################################
        
        self.cardinals = ['n','north','s','south','e','east','w','west']
        self.commands = {'s':['search'],
                    'g':['get','pickup'],
                    'd':['drop'],
                    'u':['use'],
                    'i':['inventory','backpack'],
                    'l':['look'],
                    'p':['player','stats'],
                    'm':['move','walk'],
                    'v':['view map'],
                    'h':['help','commands']}
        self.commands_verbose = ['search','get','pickup','drop','use','inventory','backpack','look','player','stats','move','walk',
                            'map','help','commands','equip']
        # ########################################################







    # ## FUNCTION for moving through gameworld ###########
    #def move_command():


    def move(self, dir_):
        def move_direction(dir_, row,column):
            #print('## DEBUG ##', dir_, rooms[room_temp['room']][3])
            if dir_[0].lower() not in self.rooms[self.room_temp['room']][3]:
                print('A wall stops you from going any further')
                self.main()
            else:
                #room_coords = [row,column]
                self.room_temp['room']= self.area[row][column]
                self.room_temp['row'] = row
                self.room_temp['column'] = column
                #print('Temporary Room Info',room_temp)

        if dir_[0] == 'e' or dir_ == 'east':
            print('Row and Column',self.row,self.column)
            self.room_temp['column'] = self.room_temp['column']+1
            move_direction(dir_, self.room_temp['row'], self.room_temp['column'])
            self.main()

        if dir_[0] == 'w' or dir_ == 'west':
            self.room_temp['column'] = self.room_temp['column']-1
            move_direction(dir_, self.room_temp['row'],self.room_temp['column'])
            self.main()

        if dir_[0] == 'n' or dir_ == 'north':
            self.room_temp['row'] = self.room_temp['row']-1
            move_direction(dir_, self.room_temp['row'], self.room_temp['column'])

        if dir_[0] == 's' or dir_ == 'south':
            self.room_temp['row'] = self.room_temp['row']+1
            move_direction(dir_, self.room_temp['row'], self.room_temp['column'])
            self.main()

        else:
            print('That does not appear to be a direction, try n,s,e,or w.')
            self.main()





    # ## PROGRAM STARTS HERE #########################################





    def main(self):

        ## Cache Room Info ##
        no_items = True

        room_title = (']ROOM: {}[\t]TURNS: {}['.format(self.rooms[self.room_temp['room']][1], next(self.times)))
        room_desc = textwrap.fill('{}'.format(self.rooms[self.room_temp['room']][2]),65)
        room_exit = ('>>The room is exited to the {}'.format(self.rooms[self.room_temp['room']][3]))
        room_exits = ('>>Exits lead to the {}.'.format(self.rooms[self.room_temp['room']][3]))

        try:
            if self.room_items[self.room_temp['room']]:
                self.room_floor = ('Items: {}'.format(self.room_items[self.room_temp['room']]['items']))
                no_items = False
        except Exception:
            pass
        #####################################################################################
        print()
        print('#'*50)
        print(room_title)
        print('')
        print(room_desc)
        inhabitant = self.creature_appearance(1, self.rooms, self.room_temp)
        print('>> ',inhabitant)

        if inhabitant[0] != 0:
            self.room_creat = inhabitant[0]

        if inhabitant[1] != False:
            if inhabitant[1] == True or self.room_temp['room'] in inhabitant[0]:
               print(inhabitant[2].format(inhabitant[0][self.room_temp['room']]['name']))
            # print('_'*50)
            # if len(self.rooms[self.room_temp['room']][3]) == 1:
            #     print(room_exit)
        else:
            if self.room_creat:
                if self.room_temp['room'] in self.room_creat:
                    print('A <{}> eyes you as you enter the room..'.format(self.room_creat[self.room_temp['room']]['name']))

        print('_'*50)
        print(room_exits)


        if no_items == False:
           for each in self.room_items[self.room_temp['room']]['items']:
               print('You see.. a {} here.'.format(each))
        print('#'*50)

        #print('-----------------------------------------------------------')
        #print(textwrap.wrap('\t{}'.format(rooms[103][1])),30)
        #print('\tExits lead.. {} and {}'.format(rooms[103][2]))
        #print('-----------------------------------------------------------')
        #print('')



        print('')
        print('\'h\' for list of commands.')
        #print('\'m\' to move. ')
        input_ = str(input('Enter a command: ')).lower().split()
        print(input_)
        if input_ != '\r' and input_ != '' and input_ !=[] and input_ !='\n':
            #print('')
            self.clr_screen()
            if input_[0].lower() in self.cardinals:
                #print('Which direction to you wish to move')
                dir_ = input_[0]
                #print('## DEBUG ## Current Room: {}:{},{}'.format(room_temp['room'],row,column))
                self.move(dir_)

            if input_[0] in self.commands_verbose and input_[0] == 'get' or input_[0] == 'drop' or input_[0] == 'equip':
               self.proccess_commands(input_[0],input_[1])

            if input_[0] in self.commands_verbose and input_ != 'm':
                #print('## DEBUG ##    Processing Commands')
                print('You Entered {}'.format(str(input_)))
                self.proccess_commands(input_[0])

            else:
                print('I don\'t recognize that command..')
                print('')
                self.main()
        else:
            print('')
            print('You entered nothing...')
            self.main()


if __name__ == "__main__":

    newgame = GameMain()
    newgame.main()




