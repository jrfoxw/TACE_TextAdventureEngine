import random as rnd
import math as mt


# ## BASIC IDEA FOR COMMANDS ###
input_=''

#
# items will temporarily be a list
# will eventually be changed to a dict to hold item info
#

items = ['sword','food','pouch','cheese','shield','stick','gems','chest','armor']
STR = mt.ceil(rnd.randrange(6,20))
DEX = mt.ceil(rnd.randrange(6,20))
CON = mt.ceil(rnd.randrange(6,20))
stats = [STR,DEX,CON]
area = []
backpack = []


# # DEFINE LISTS #########################################
gold = []
commands = {'S':'search',
            'G':'get',
            'D':'drop',
            'U':'use',
            'I':'inventory',
            'L':'look',
            'P':'player'}
# ########################################################

# ## FUNCTION FOR TESTING VALUE OF COMMANDS ##############
def proccess_commands(input_):
    if commands[input_] == 'search':
        search_command()
        main()
        return 
    elif commands[input_] == 'get':
        get_command()
        main()
    elif commands[input_] == 'inventory':
        inventory_command()
        main()
    elif commands[input_] == 'look':
        look_command()
        main()
    elif commands[input_] == 'player':
        player_command()
        main()
    elif commands[input_] == 'drop':
        drop_command()
        main()
    else:
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

# ## FUNCTION for using get command #####################
def get_command():
    print('what do you wish to pick-up?')
    focus = input('?: ')
    if focus in area:
        print('you pick up the {} and place it in your backpack!'.format(focus))
        area.remove(focus)
        backpack.append(focus)
        print('DEBUG### carried value = {}'.format(len(backpack)))
    else:
        print('I don\'t see anything like that.')
        
def drop_command():
    print('')
    print('What item do you wish to drop?')
    release = input('?: ')
    if release in backpack:
        have = backpack.index(release)
        backpack.pop(have)
        area.append(release)
        print('You drop the {} on the ground'.format(release))
            
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
    print('Current Stats:')
    print('\tSTR - {}'.format(stats[0]))
    print('\tDEX - {}'.format(stats[1]))
    print('\tCON - {}'.format(stats[2]))
    return


# ## FUNCTION for randomizing items on ground ###########
def random_items():
    chance = mt.ceil(rnd.randrange(1,13))
    if chance >6:
        item = mt.floor(rnd.randrange(0,len(items)))
        print('DEBUG###  item value = {}'.format(item))                
        print('\tyou see a *{}* on the ground'.format(items[item]))
        area.append(items[item])
    return

# ## PROGRAM STARTS HERE #########################################

def main():
    
    print('')
    for command in commands.keys():
        print('{:5}{:15}'.format(command,commands[command]))
    print('')
    input_ = input('Enter a command: ').upper()
    print('')    
        
    if input_ in commands.keys() or input_ in commands.values():
        print('You selected {}'.format(commands[input_]))
        proccess_commands(input_)
        main()
    else:
        print('I don\'t recognize that command..')
        print('')
        main()
    

main()
            
    
    
    
    