# -*- coding: utf-8 -*-
"""
baccarat.py

Created on Thu Jul 30 2015

@author: amaloney
"""

banker = 0
ties = 0
player = 0
input_file = open('bacShoes1-5.txt')
for line in input_file:
    shoe = line.strip().split(',')
#    print(shoe)
    print('Shoe #', shoe.pop(0),'had ', end = '')
    print(len(shoe), 'hands.')
    for result in shoe:
        if result == 'T':
            ties += 1
        elif result == 'B':
            banker += 1
        else:
            player += 1
    print("P ", player, " B ", banker, " T ", ties)
    banker = player = ties = 0

input_file.close()
    