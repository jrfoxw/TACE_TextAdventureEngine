from __future__ import print_function
import texttable as tt
from random import choice
from random import randrange as rrange
from name_creator_elf import namebuilder
import sqlite3
import textwrap as tw
from libs.commands import GameCommLib
from libs.items import *
from libs.utils import GameUtils
from libs.player import GamePlayer
from libs.creatures import GameCreatures


class GameMain(GameCommLib, GameCreatures, GamePlayer, GameUtils):

    def __init__(self):
        GameCommLib.__init__(self)
        GameUtils.__init__(self)
        GameItems.__init__(self)
        GamePlayer.__init__(self)
        GameCreatures.__init__(self)

        """
            CONNECT TO DATABASE AND RETRIEVE ROOM DATA
        """
        self.player_name = namebuilder(3, 9)
        self.last_name = namebuilder(5, 8)

        self.connect_db = sqlite3.connect('SQL_COMMAND_DEMO.db')
        # print(self.connect_db)
        self.conn = self.connect_db.cursor()
        self.grab = self.conn.execute("SELECT * FROM 'ROOMS'")


        self.column_name = self.grab.description
        self.stored_rooms_data = sorted(self.grab.fetchall())

        # print('Stored Rooms Data == {}'.format(self.stored_rooms_data))

        self.area = [
                 ['#','#','#','#','#'],
                 ['#','#',106,'#','#'],
                 ['#',101,102,'#','#'],
                 ['#',103,104,107,'#'],
                 ['#',105,'#','#','#'],
                 ['#','#','#','#','#']


                ]
        self.room_creat = {}
        self.inhabit_by = ''
        self.column = 1
        self.row = 2
        self.times = self.turn()



        # # SQLite ROOMS data # #
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
        self.\
            commands_verbose = ['search','get','pickup','drop','use','inventory','backpack','look','player','stats','move','walk',
                            'map','help','commands','equip']
        self.arg_commands = ['examine', 'get', 'drop', 'use', 'equip', 'pickup']
        self.base_commands = ['search','inventory', 'backpack', 'look', 'stats', 'map', 'help', 'commands', 'player']

    # UPDATES ANY CHANGES TO GRID #
    """
        Assign Main Room
        start = starting room (int)
    """

    def update_grid(self, start=104):
        for x in range(len(self.area)):
            for y in range(len(self.area[x])):
                if self.area[x][y] == start:
                    self.room_temp = {'room': start, 'row': x, 'column': y}

    # ### MOVE ### #
    """
        Function for moving through game grid
    """

    def move(self, dir_):

        def move_direction(dir_, row, column):
            #print('## DEBUG ##', dir_, rooms[room_temp['room']][3])
            if dir_[0].lower() not in self.rooms[self.room_temp['room']][3]:
                self.response('A wall stops you from going any further')
                self.main()
            else:
                #room_coords = [row,column]
                self.room_temp['room']= self.area[row][column]
                self.room_temp['row'] = row
                self.room_temp['column'] = column
                #print('Temporary Room Info',room_temp)

        if dir_[0] == 'e' or dir_ == 'east':
            # DEBUG
            print('Row and Column', self.row, self.column)
            self.room_temp['column'] = self.room_temp['column']+1
            move_direction(dir_, self.room_temp['row'], self.room_temp['column'])
            self.response('You head {}...'.format(dir_))
            self.main()

        if dir_[0] == 'w' or dir_ == 'west':
            self.room_temp['column'] = self.room_temp['column']-1
            move_direction(dir_, self.room_temp['row'],self.room_temp['column'])
            self.response('You head {}...'.format(dir_))
            self.main()

        if dir_[0] == 'n' or dir_ == 'north':
            self.room_temp['row'] -= 1
            move_direction(dir_, self.room_temp['row'], self.room_temp['column'])
            self.response('You head {}...'.format(dir_))
            self.main()

        if dir_[0] == 's' or dir_ == 'south':
            self.room_temp['row'] = self.room_temp['row']+1
            move_direction(dir_, self.room_temp['row'], self.room_temp['column'])
            self.response('You head {}...'.format(dir_))
            self.main()

        # else:
        #     print('That does not appear to be a direction, try n,s,e,or w.')
        #     self.main()

    # ## PROGRAM STARTS HERE #########################################

    def intro(self):
        self.intro_done = False
        get_name = """\n\n\n
        Before we begin, a few questions if you would?
        What name would you like your player to be called?
        If you prefer not to choose a name;
        a random one will be assigned to your player.
        Do you wish to choose a name? (Y/N)
        """
        g_name = input(get_name)
        if g_name == "Y":
            self.player_name = input('Please enter a name. > ')
        else:
            self.player_name = namebuilder(3, 8)



        self.clr_screen(10)
        room_title = ('\t]{}[\t\t]TURNS: {}[\t\t] SCORE: 0['.format(self.rooms[self.room_temp['room']][1], 0))
        room_exit = ('>>The room is exited to the {}'.format(self.rooms[self.room_temp['room']][3]))
        room_exits = ('>>Exits lead to the {}.'.format(self.rooms[self.room_temp['room']][3]))
        room_break = """-#"""*50

        intro_ = """{0}\n {1}\n\n\n
                              THE PASSAGE
                               CHAPTER 1
                            "INTO THE DEPTHS"

        You awaken...

        Your head aches as you try to stand, you rub the back of your neck
        discovering a large, and somewhat sensitive bump at the base of your
        skull. Blurry-eyed you attempt to get your bearings, realizing that
        nothing around you appears remotely familiar...


        """.format(room_title, room_break, room_break, room_exit)
        # text_intro = tw.TextWrapper()
        # text_intro.width = 50
        # text_intro.fill = intro_
        # text_intro = tw.fill(intro_, 85)

        print(intro_)

    def main(self):

        # # Cache Room Info # #
        no_items = True
        room_break = """-#"""*50
        room_title = ('\t]{}[\t\t]TURNS: {}[\t\t] SCORE: 0[\t\t] ROOM: {}['.format(self.rooms[self.room_temp['room']][1],
                                                                                   next(self.times),
                                                                                   self.rooms[self.room_temp['room']][0]))
        room_desc = tw.fill('{}'.format(self.rooms[self.room_temp['room']][2]), 68)
        room_exit = ('>>The room is exited to the {}'.format(self.rooms[self.room_temp['room']][3]))
        room_exits = ('>>Exits lead to the {}.'.format(self.rooms[self.room_temp['room']][3]))

        try:
            if self.room_items[self.room_temp['room']]:
                self.room_floor = self.response(('Items: {}'.format(self.room_items[self.room_temp['room']]['items'])))
                no_items = False
        except Exception:
            pass

        print()

        # print('{}'.format(room_title))
        # print('')
        # print(room_desc)
        inhabitant = self.creature_appearance(1, self.rooms, self.room_temp)
        # print('Inhabitant data: ', inhabitant)
        # print('>> ', inhabitant[0])

        if inhabitant[0] != 0:
            self.room_creat = inhabitant[0]

        if inhabitant[1] != False:
            if inhabitant[1] == True or self.room_temp['room'] in inhabitant[0]:
                self.inhabit_by = inhabitant[2].format(inhabitant[0][self.room_temp['room']]['name'])
            # print('_'*50)
            # if len(self.rooms[self.room_temp['room']][3]) == 1:
            #     print(room_exit)
        else:
            if self.room_creat:
                if self.room_temp['room'] in self.room_creat:
                    self.inhabit_by = 'A <{}> eyes you as you enter the room..'.\
                                        format(self.room_creat[self.room_temp['room']]['name'])

        # print('_'*50)
        # print(room_exits)

        if self.intro_done != True:
            self.intro_done = True
            describe = """{2} \n\n {3} \n{4} \n{5}""".format(room_title,
                                                             room_break,
                                                             tw.indent(room_desc,'\t\t'),
                                                             room_break,
                                                             room_exit,
                                                             self.inhabit_by)

            print(describe)
        else:
            describe = """{0}\n {1}\n\n\n {2} \n\n {3} \n{4} \n{5}""".format(room_title,
                                                                             room_break,
                                                                             tw.indent(room_desc,'\t\t'),
                                                                             room_break,
                                                                             room_exit,
                                                                             self.inhabit_by)
            print(describe)

        if no_items is False:
            for each in self.room_items[self.room_temp['room']]['items']:
                self.response('You see.. a {} here.'.format(each))

        """
            PROCESS INPUT
        """
        def process_input():
            self.clr_screen(5)
            input_comm = str(input('Enter a command: ')).lower()
            input_ = input_comm.split()
            #print('input >> ', input_)

            """ check for empty input """
            if input_ == '\r' \
                    or input_ != '' \
                    or input_ != [] \
                    or input_ != '\n':
                self.response('You entered nothing..')
                self.main()

            elif input_[0].lower() in self.cardinals:
                dir_ = input_[0]
                # print('## DEBUG ## Current Room: {}:{},{}'.format(room_temp['room'],row,column))
                self.move(dir_)
                """ check for commands that take args """

            elif input_[0] in self.arg_commands:
                input_verb = input_[0]

                """ separate input into verb and nouns """
                if len(input_) != 1:
                    for each in input_:
                        if each in self.arg_commands:
                            input_noun = input_comm.split(each+' ')
                            #print('verb:{1} noun:{0}'.format(input_noun[1], input_verb))
                            self.proccess_commands(input_[0], input_noun[1])
                            self.main()
                else:
                    self.response("{} what?".format(input_[0]))
                    self.main()

                    """ check for base commands """
            elif input_[0] in self.base_commands:
                self.proccess_commands(input_[0])
                self.main()

            else:
                self.response('I don\'t recognize that command..')
                print('')
                self.main()

        process_input()


if __name__ == "__main__":

    newgame = GameMain()
    newgame.intro()
    newgame.update_grid(newgame.room_select)
    newgame.main()




