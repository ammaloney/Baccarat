# -*- coding: utf-8 -*-
"""
baccaratDataFileReader.py
Created on Mon Dec 21 20:49:04 2015

@author: amaloney
"""

from collections import Counter
import itertools

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

file_in = open(file_path, 'r')
cont = True
while cont:
    
    aShoe = file_in.readline()
    aShoe = aShoe[:-1]
    print(aShoe)
    count = Counter(aShoe)
    for hand in count:
        if hand == 'P': print('Player', count['P'], end = ' ')
        if hand == 'p': print('Panda', count['p'], end = ' ')
        if hand == 'B': print('Banker', count['B'], end = ' ')
        if hand == 'D': print('Dragon', count['D'], end = ' ')
        if hand == 'T': print('Tie', count['T'])
    
    if aShoe[0].isdigit() == False:
        shoe = ([''.join(value) for key, value in itertools.groupby(aShoe)])
        for streak in shoe:
            print(streak)
        frequency = Counter(shoe)
        print(frequency)
        
    temp = input('Enter "n" to stop')
    if temp[0].lower() == 'n':
       cont = False


file_in.close()
