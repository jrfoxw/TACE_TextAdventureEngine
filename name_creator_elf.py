import random as rnd
import math as mt



def namebuilder(sizem=3, sizex=7):
    vowels = [96,97,101,105,111,117,121]
    namefull = []
    part1 = ['sh','te','ta','tu','ti','tr','to']    
   
    sized = int(mt.floor(rnd.randint(sizem,sizex)))
    for length in range(0,sized):
        if length == 1:
            rand_vowel = int(mt.floor(rnd.randint(0,5)))
            namefull.append(chr(vowels[rand_vowel]))
        constants = int(mt.floor(rnd.randint(97,119)))
        namefull.append(chr(constants))
    for x in range(0,len(namefull)):
        nim = (''.join(namefull).capitalize())
    return nim    
     
    
        


        
        
    
