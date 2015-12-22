# -*- coding: utf-8 -*-
"""
baccaratDataFileReader.py
Created on Mon Dec 21 20:49:04 2015

@author: amaloney
"""

from collections import Counter

file_in = open('data.out', 'r')

aShoe = file_in.readline()
aShoe = aShoe[:-1]
print(aShoe)
count = Counter(aShoe)
for hand in count:
    if hand == 'P': print('Player', count['P'])
    if hand == 'p': print('Panda', count['p'])
    if hand == 'B': print('Banker', count['B'])
    if hand == 'D': print('Dragon', count['D'])
    if hand == 'T': print('Tie', count['T'])


file_in.close()
