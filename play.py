#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 22:19:23 2018

@author: wfarah
"""

import numpy as np
from snake.game import Snake,GameLostException,GameWonException
from snake.gui import gameGUI
from snake.game.utils import numToLetter

def play():
    snake = Snake(dimension=10,start_size=5,survivalmode=True)
    gui = gameGUI()
    
    board = snake.returnBoard(trimmed = True)

    gui.updateFrame(board)
    gameover = 0

    while not gameover:       
        #inp = raw_input("How to move? (u,d,l,r):")
        r = np.random.randint(4)
        inp = numToLetter(r)
        #time.sleep(1)
#        if inp not in ["u","d","l","r"]:
#            print "Error, input u,d,l or r only"
#            continue
        try:
            snake.move(inp)
        except GameLostException as e:
            raise e
        except GameWonException as e:
            raise e
            
        board = snake.returnBoard(trimmed = True)
        gui.updateFrame(board)

if __name__ == "__main__":
    while True:
        try:
            play()
        except GameLostException as e:
            print e
            pass
        
        
