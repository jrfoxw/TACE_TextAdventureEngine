import math
import random
from sys import exit
import textwrap
from shutil import get_terminal_size


level_001 = [
              ['#','#','#','#'],
              ['#',101,102,'#'],
              ['#',103,104,'#'],
              ['#','#','#','#']
            ]

visited =[]

# Just some basic rooms, room 103 has a trap in it, thus the True statement
# Room: 0:Room Short, 1:Trap = False, 2:Description, 3:Blocked = False, 4:Exits

level_001_description = {
                          100:['PURGATORY',False,'Purgatory not a good place to be.',False,''],  # Not defined on the map, used as a holding place. 
                          101:['Big Room',False,'This room is really big, like most big rooms would be. It is oddly shaped, unlike how most big rooms are, and it smells quite bad. Like someone left an old, well-used shoe lying around.',False,'east and south.'],
                          102:['Small Room',False,'You see why it\'s called the small, room because its really, really small. There are old odd statues on one wall, silently staring at the adjacent wall.',False,'west and south.'],
                          103:['Tiny Room',True,'A big tiny room with nothing small in it. which is odd, because you would think that a tiny room, would only have tiny stuff in it. The only thing of interest is a bubbling fountain in the middle of the tiny room. The floor makes a odd creaking noise as you walk across it.',False,'east and north.'],
                          104:['Long Room',False,'Wow the descriptions for these rooms, I wonder what architect came up with the very obvious names, suffice it to say; this room is really really long. Only item that pops out at you is a strange looking pedestal with nothing on it.',False,'west and north']

                        }


huhs = ['You want to do what?','I have no clue what you are asking','Huh?','Right..sure','You might want to choose a command','No, its obvious you have no clue what you are doing..','Maybe if you actually made a choice, something would happen? Just saying..']

accepted_comm = ['g','grab','p','pickup','t','throw','d','drop','h','help','look','s','search','q','quit','kill','k',
                 'crush','destroy','grab']
command = {'s':['search','look'],'g':['get'],'p':['pickup'],'t':['throw'],'d':['drop'],'h':['help'],'m':['move'],'q':['quit'],'k':['kill','crush','destroy']}


def crush(level,describe,room,column,row):
   kill(level,describe,room,column,row)
   
def destroy(level,describe,room,column,row):
   kill(level,describe,room,column,row)

def drop(level,describe,room,column,row):
   print('you drop something on your toe')

def get(level,describe,room,column,row):
   pass
   

def grab(level,describe,room,column,row):
   get(level,describe,room,column,row)

def help(level,describe,room,row,column):
   for comm in command:
      for each in range(len(command[comm])):
         print('{:5}{}'.format(comm,command[comm][each]))
def huh(level,describe,room,row,column):
   says = random.randrange(len(huhs))
   print(huhs[says])
   main(level,describe,room,row,column)
   
   

def kill(level,describe,room,column,row):
   kill_randomly = random.randrange(21)
   if kill_randomly <=7:
      text = ('You are determined to kill something, what you don\'t know, but you do know this... it will happen..')
      print(textwrap.fill(text,45))
   if kill_randomly >=8 and kill_randomly <=14:
      text = ('You look in the {} around for something to kill, finding nothing you determine that smashing a good solid rock will do the trick. At first its gratifying but soon after you realize it\'s no fun without that satisfying crunch...'.format(describe[room][0]))
      print(textwrap.fill(text,45))
   if kill_randomly >=15:
      text = ('You unmercifully shake your fist at the wall, it obviously is filled with terror as it stands frozen in fear...')
      print(textwrap.fill(text,45))

def look(level,describe,room,column,row):
   print('You look around the area')
   search(level,describe,room,row,column) # similar to 'search' calls the search() function. 
   

def pickup(level,describe,room,column,row):
   print('You pickup')

def trap():
   traps = random.randrange(100)
   print()
   if traps <=50:
      text = ('You didn\'t even see it coming, the floor gives way under you feet, and as you plummet in to the inky blackness below, you only have on thought on your mind... "So that\'s why the floor creaks!"')
      print(textwrap.fill(text,45))
      print()
      score()
   else:
      print('You feel for some reason that you have avoided a gruesome fate...')
   
   
def throw(level,describe,room,column,row):
   print('you throw something')
   
def search(level,describe,room,row,column):
   print('You search the {}'.format(level_001_description[room][0])) 
   gold = random.randint(1,100)
   print('You found {} gold!'.format(gold))

def score():
   print('You suck')
   print('Your score is a big fat 0!')
   print('Why? Because I haven\'t implemented a scoring system yet >_<')
   
   again = input('Play again (y/n) ?:')
   if again == 'y':
      main(level_001,level_001_description,101,1,1)
   else:   
      return
   



# THE MAIN FUNCTION FOR THE PROGRAM, PROCESS ALL COMMANDS THEN RUN APPROPRIATE FUNCTION #
def main(level,describe,room,row,column):
   
   
   
   print()
   print('-- ]{}[ --'.format(describe[room][0]))
   print('______________________________________________')
   if room not in visited:
      text = ('{}'.format(describe[room][2]))
      print(textwrap.fill(text,45))
      print('______________________________________________')
      print('-exits lead {}-'.format(describe[room][4]))
      visited.append(room)
      print(visited)
      if describe[room][1] != False:
         trap()
         
   print()
   input_ = input('Command ?: ')
   print("\n" * get_terminal_size().lines, end='')
                                                            
   """
   
   
   # move is a special command and does not get processed here
   # does the user input exist in our accepted list accepted_comm[] ?
   # if it does we need to evaluate what command it is
   # we do this by iterating through the dict command{} 
   # if the user input is found in command{} then we 
   # we need to assign the value of input_ to the value
   # of the first command in command{} keys values.
   
   
   """
   if input_ in accepted_comm and input_ !='move' and input_[0] != 'q':          
      for comm in command:                                  
         for each in range(len(command[comm])):                            
            if input_ in command[comm][each]:                
               input_ = command[comm][each]                  
                                                            
               
               # DEBUG # print('The command you entered is {}'.format(input_))     
               print()
               eval(input_+'(level,describe,room,row,column)') # <---VERY IMPORTANT TURNS INPUT_ IN TO A USABLE FUNCTION CALL @
               main(level,describe,room,row,column)
            
               """
               @ Here is where the move command is processed
               @ first we determine if the user has entererd the move command
               @ we do this two ways, see if the user has entered the single character or typed the entire word.
               @ Typically you would only have to use the single character.
               @ Next we just print out a message, for debug purposes showing that the move command
               @ has been succesfully recognized.
               @_____________________________
               @ PROCESS CARDINAL DIRECTIONS
               @_____________________________
               @ The next step is to process the cardinal directions
               @ in this case for simplicty sake we are only using N,S,E,W
               @ Since we are only using a 2D column and row system we need to first establish 
               @ where the character is on the map
               @ we do this by using an if statement to see if the characters next move
               @ will end up out of bounds.
               @ 
               @ Before that we go ahead and add one to the column, since we are moving
               @ east the columns increases in this case from 1 to 2.
               @ however we still need to check to verify that we are not making an 
               @ illegal move.
               @
               @ if the move is illegal we don't want anything to change, and we want
               @ the character to stay in the room they are in.
               @ therefore we change the column from 2 to 1
               @ and give and indication to the player that they cannot move 
               @ in that direction.
               @ 
               @ if there is no wall in our next move we simply pass to the
               @ else statement. Once again we indicate to the player that
               @ they have succesfully moved.
               @
               @
               @ You might be asking:
               @ 'How do we establish where the character is in the first place?'
               @ 
               @ Simply place your players starting position in the main() call 
               @ at the starte of th program. It will then be carried out 
               @ and changed dynamically based on movements and actions.
               @
               
                          

               """
               
   elif input_ == '' or input_ == ' ':
      huh(level,describe,room,row,column)
   
   elif input_[0] == 'q' or input_ == 'quit':
      score()
   elif input_ == 'move' or input_[0] == 'm':
      print('You move around for a bit')
      dir = input('Direction ?: ')
      
      if 'e' in dir[0]: 
         column +=1
         if level[row][column] =='#':
            column -=1
            room = level[row][column]
            print('You can\'t go that way...')
            main(level,describe,room,row,column)
         else:
            room = level[row][column]
            print('You head east...')
            main(level,describe,room,row,column)
            
         
      if 'w' in dir[0]:
         column -=1
         if level[row][column] =='#':
            column +=1
            room = level[row][column]             
            print('You can\'t go that way...')
            main(level,describe,room,row,column)
         else:
            room = level[row][column]
            print('You head west...')
            main(level,describe,room,row,column)
         
      if 'n' in dir[0]: 
         row -=1
         if level[row][column] =='#':
            row +=1
            room = level[row][column]             
            print('You can\'t go that way...') 
            main(level,describe,room,row,column)
         else:
            room = level[row][column]
            print('You head north...')
            main(level,describe,room,row,column)
         
      if 's' in dir[0]:
         row +=1
         if level[row][column] =='#':
            row -=1
            room = level[row][column]             
            print('You can\'t go that way...')
            main(level,describe,room,row,column)
         else:
            room = level[row][column]
            print('You head south...')
            main(level,describe,room,row,column)
         
         
    
    
      if dir[0] !='e' and dir[0] !='w' and dir[0] !='n' and dir[0] !='s': 
         print('That is not a direction...')
         main(level,describe,room,row,column)
      
   else:
      print('I\'m not familar with that command..')
      main(level,describe,room,row,column)



# RUN OUR PROGRAM ##########   
if __name__ == '__main__':
   print("\n\n" * get_terminal_size().lines, end='')
   main(level_001,level_001_description,101,1,1)   
   