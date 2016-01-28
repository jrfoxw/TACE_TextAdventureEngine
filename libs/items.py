import math as mt
import random as rnd
from random import randrange as rrange


__author__ = 'PY-DEV'


class GameItems:

    def __init__(self):
        self.items = ['food', 'pouch', 'cheese', 'gems', 'chest', 'vial']
        self.room_items = {100: {'items': ['none']}}

    #  FUNCTION for randomizing items on ground #

    def random_items(self, room_temp=dict):
        chance = mt.ceil(rnd.randrange(1, 13))
        if chance > 3:

            item = rrange(0,len(self.items))
            # print('## DEBUG ##  item value = {}'.format(item))
            print('\tyou see a *{}* on the ground'.format(self.items[item]))
            # backpack.append(items[item])
            # try:
            if room_temp['room'] in self.room_items.keys():
                # print('## DEBUG ## Try ITEMS',room_items)
                self.room_items[room_temp['room']]['items'].append(self.items[item])
            # except Exception as inst:
            else:
                # print(inst)
                self.room_items[room_temp['room']] = {'items': [self.items[item]]}
                # print('## DEBUG ## except ITEMS',room_items)

        return

