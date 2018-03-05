#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 16:13:37 2018

@author: wfarah
"""

import matplotlib.pyplot as plt

class gameGUI(object):
    def __init__(self):
        self.fig = plt.figure(1,figsize=(10,14))
        plt.ion()
        plt.show()
    def updateFrame(self,board,pause=0.001):
        self.fig.clf()
        plt.imshow(board,interpolation='nearest',
                   aspect='auto')
        plt.pause(pause)

