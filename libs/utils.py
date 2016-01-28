
from random import randrange as rrange
import textwrap as tw

class GameUtils:

    def turn(self):
            for turns in range(1000):
                yield turns

    def clr_screen(self, lines=55):
        for x in range(lines):
            print('')


    def die_roll(self, num=1):
        die1 = rrange(10)
        die2 = rrange(10)

        roll = int(str(die1)+str(die2))

        return roll

    def response(self, text):
        texta = tw.fill(text, 70)
        textlen = 10+len(text)

        print("="*85)
        print(" {} \t".format(texta))
        print("="*85)
