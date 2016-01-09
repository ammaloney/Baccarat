# -*- coding: utf-8 -*-
"""
baccarat.py

Created on Thu Jul 30 2015

@author: amaloney
"""

banker = 0
bankerTotal = 0
ties = 0
tiesTotal = 0
player = 0
playerTotal = 0
totalHandsDealt = 0
shoeNumber = 0 

try:
    with open('bac-sim-25k-1.txt', 'r') as data:
        for line in data:
            shoe = line.strip().split(',')
            try:
                shoeNumber = int(shoe.pop(0))
                print('Shoe #', shoeNumber,'had ', len(shoe), 'hands: ', end ='')
                for result in shoe:
                    if result == 'T':
                        ties += 1
                    elif result == 'B':
                        banker += 1
                    else:
                        player += 1
                print("P ", player, " B ", banker, " T ", ties)
                bankerTotal += banker
                tiesTotal += ties
                playerTotal += player
                banker = player = ties = 0
            except ValueError as err:
                pass
except IOError as err:
    print('File error: ' + str(err))

totalHandsDealt = bankerTotal + tiesTotal + playerTotal

print(str(totalHandsDealt), 'hands dealt.', 
      'Average', str(totalHandsDealt / 25000))
print('Total banker wins', str(bankerTotal), 
      'Ratio: {:1.6f}'.format((bankerTotal / totalHandsDealt)))
print('Total player wins', str(playerTotal), 
      'Ratio: %1.6f' % (playerTotal / totalHandsDealt))
print('Total  tie  hands', str(tiesTotal), 
      'Ratio: %1.6f' % (tiesTotal / totalHandsDealt))
