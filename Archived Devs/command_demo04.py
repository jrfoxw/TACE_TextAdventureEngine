from __future__ import print_function
import random as rnd
import math as mt
from name_creator_elf import namebuilder
import textwrap

# ## BASIC IDEA FOR COMMANDS ###
input_=''

#
# items will temporarily be a list
# will eventually be changed to a dict to hold item info
#


player_name = namebuilder(3,9)
last_name = namebuilder(5,8)
items = ['sword','food','pouch','cheese','shield','stick','gems','chest','armor']
STR = mt.ceil(rnd.randrange(6,20))
DEX = mt.ceil(rnd.randrange(6,20))
CON = mt.ceil(rnd.randrange(6,20))
stats = [STR,DEX,CON]
area = [
         ['#','#','#','#'],
         ['#',101,102,'#'],
         ['#',103,104,'#'],
         ['#',105,'#','#'],
         ['#','#','#','#']


        ]
backpack = []
column = 1
row = 2

room_temp = {'room':103,'row':2,'column':1}
room_coords = [row,column]
rooms = {101:['White Room','a small white room.','south and east',['s','e']],
         102:['Red Room','a small red room with a window','west',['w']],
         103:['Fountain Room',"""You enter a open air room with a fountain,
                               the water cascades down the statue
                               of a unknown warrior dressed in
                               armor of an ancient empire, long ago
                               gone.""",'north, south and east',['n','e','s']],
         104:['Strange Room','a strange room with odd markings','west',['w']],
         105:['Small Banquet Hall',"""Entering this room is no small feat, as you clamber over broken, overturned tables; splintered, yet finely tapestried chairs. All of which appear to have been left behind, quickly and with reckless abandon...""",
              'north',['n']],


         }

room_items = {100:{'items':['none']}}

world="""
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
gold = []
cardinals = ['n','north','s','south','e','east','w','west']
commands = {'s':['search'],
            'g':['get','pickup'],
            'd':['drop'],
            'u':['use'],
            'i':['inventory','backpack'],
            'l':['look'],
            'p':['player','stats'],
            'm':['move','walk'],
            'v':['view map'],
            'h':['help','commands']}
commands_verbose = ['search','get','pickup','drop','use','inventory','backpack','look','player','stats','move','walk',
                    'view map','help','commands']
# ########################################################

# ## FUNCTION FOR TESTING VALUE OF COMMANDS ##############
def proccess_commands(input_):

    commands_proc[input_]()
    main()


# ## FUNCTION for using search command ###################
def search_command():
    print('you search the area and find...')
    random_items()
    fate = mt.ceil(rnd.randrange(1,15))
    if fate >= 8:
        coins = mt.floor(rnd.randrange(5,25))
        print('\t{} gold coins!'.format(coins))
        gold.append(coins)
        print('\tYou have a total of {} gold coins'.format(sum(gold)))
        print('')
    else:
        print('Nothing else of importance..')
    return

# ## FUNCTIONs for using get/drop command #####################
def get_command():
    print('what do you wish to pick-up?')
    focus = input('?: ')
    if focus in room_items[room_temp['room']]['items']:
        print('you pick up the {} and place it in your backpack!'.format(focus))
        room_items[room_temp['room']]['items'].remove(focus)
        backpack.append(focus)
        print('DEBUG### carried value = {}'.format(len(backpack)))
    else:
        print('I don\'t see anything like that.')

def drop_command():
    print('')
    print('What item do you wish to drop?')
    release = input('?: ')
    if release in backpack:
       backpack.remove(release)
       print('You drop the {} on the ground'.format(release))
       room_items[room_temp['room']]['items'].append(release)

    else:
        print('I don\'t see that item in your inventory.')


# ## FUNCTION for using inventory command #####################
def inventory_command():
    x = 0
    print('')
    print('\t<<<<<<IVENTORY>>>>>')
    print('')
    if len(backpack) >0:
        print('')
        for item in backpack:
            x +=1

            print('\t{:5} --- {}'.format(x,item))
        print('\tyou are carrying {}gp in coins'.format(sum(gold)))
    else:
        print('\tThere is nothing in your backpack..')
        print('\tyou are carrying {}gp in coins'.format(sum(gold)))


# ## FUNCTION for using look command #####################
def look_command():
    print('')
    print('\tlooking around you see:')
    if len(area) >0:
        for things in area:
            print('\t{},'.format(things),end='')
        print('')
    else:
        print('\tYou see a lot of dirt, nothing else just dirt!')
    return

# ## FUNCTION for using player command #####################
def player_command():
    print('')
    print('Name: {} {}'.format(player_name,last_name))
    print('')
    print('Current Stats:')
    print('\tSTR - {}'.format(stats[0]))
    print('\tDEX - {}'.format(stats[1]))
    print('\tCON - {}'.format(stats[2]))
    return


# ## FUNCTION for randomizing items on ground ###########
def random_items():
    chance = mt.ceil(rnd.randrange(1,13))
    if chance >3:
        item = mt.floor(rnd.randrange(0,len(items)))
        #print('## DEBUG ##  item value = {}'.format(item))
        print('\tyou see a *{}* on the ground'.format(items[item]))
        #backpack.append(items[item])
        #try:
        if room_temp['room'] in room_items.keys():
           #print('## DEBUG ## Try ITEMS',room_items)
           room_items[room_temp['room']]['items'].append(items[item])
        #except Exception as inst:
        else:
            #print(inst)
            room_items[room_temp['room']] = {'items':[items[item]]}
            #print('## DEBUG ## except ITEMS',room_items)



    return

# ## FUNCTION for moving through gameworld ###########
#def move_command():


def move(dir_):
    def move_direction(dir_,row,column):
        print('## DEBUG ##', dir_, rooms[room_temp['room']][3])
        if dir_[0].lower() not in rooms[room_temp['room']][3]:
            print('A wall stops you from going any further')
            main()
        else:
            #room_coords = [row,column]
            room_temp['room']= area[row][column]
            room_temp['row'] = row
            room_temp['column'] = column
            #print('Temporary Room Info',room_temp)

    if dir_[0] == 'e' or dir_ == 'east':
        print('Row and Column',row,column)
        room_temp['column'] = room_temp['column']+1
        move_direction(dir_, room_temp['row'], room_temp['column'])
        main()

    if dir_[0] == 'w' or dir_ == 'west':
        room_temp['column'] = room_temp['column']-1
        move_direction(dir_, room_temp['row'],room_temp['column'])
        main()

    if dir_[0] == 'n' or dir_ == 'north':
        room_temp['row'] = room_temp['row']-1
        move_direction(dir_, room_temp['row'], room_temp['column'])

    if dir_[0] == 's' or dir_ == 'south':
        room_temp['row'] = room_temp['row']+1
        move_direction(dir_, room_temp['row'], room_temp['column'])
        main()

    else:
        print('That does not appear to be a direction, try n,s,e,or w.')
        main()





# List Commands ################################################
def help_command():
    for command in commands.keys():
        print('{}: {}'.format(command,commands[command][0]))


# ## PROGRAM STARTS HERE #########################################


def clr_screen():
    for x in range(55):
        print('')

commands_proc = {'search':search_command,'get':get_command,'drop':drop_command,'inventory':inventory_command,
                 'help':help_command,'look':look_command,'stats':player_command}

def main():

    no_items = True
    room_title = (']{}['.format(rooms[room_temp['room']][0]))
    room_desc = textwrap.fill('{}'.format(rooms[room_temp['room']][1]),65)
    room_exit = ('>>The room is exited to the {}'.format(rooms[room_temp['room']][2]))
    room_exits = ('>>Exits lead to the {}.'.format(rooms[room_temp['room']][2]))
    try:
        if room_items[room_temp['room']]:
            room_floor = ('Items: {}'.format(room_items[room_temp['room']]['items']))
            no_items = False
    except Exception:
        pass

    print()
    print('#'*50)
    print(room_title)
    print('')
    print(room_desc)
    print('_'*50)
    if len(rooms[room_temp['room']][3]) == 1:
        print(room_exit)
    else:
        print(room_exits)
    if no_items == False:
       for each in room_items[room_temp['room']]['items']:
           print('You see.. a {} here.'.format(each))
    print('#'*50)

    #print('-----------------------------------------------------------')
    #print(textwrap.wrap('\t{}'.format(rooms[103][1])),30)
    #print('\tExits lead.. {} and {}'.format(rooms[103][2]))
    #print('-----------------------------------------------------------')
    #print('')



    print('')
    print('\'h\' for list of commands.')
    print('\'m\' to move. ')
    input_ = input('Enter a command: ').lower()

    print('')
    clr_screen()
    if input_.lower() in cardinals:
        #print('Which direction to you wish to move')
        dir_ = input_
        #print('## DEBUG ## Current Room: {}:{},{}'.format(room_temp['room'],row,column))
        move(dir_)


    if input_ in commands_verbose and input_ != 'm':
        #print('## DEBUG ##    Processing Commands')
        print('You Entered {}'.format(input_))
        proccess_commands(input_)

    else:
        print('I don\'t recognize that command..')
        print('')
        main()


main()




