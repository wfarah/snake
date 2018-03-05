#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 12:46:49 2018

@author: wfarah
"""

import numpy as np

def oneHotVector(letter):
    if not isinstance(letter,str):
        raise TypeError("Letter should be string, %s (%s) given"
                        %(letter, type(letter)))
    if letter == "d":
        return np.array([0,0,1,0])
    elif letter == "u":
        return np.array([1,0,0,0])
    elif letter == "l":
        return np.array([0,0,0,1])
    elif letter == "r":
        return np.array([0,1,0,0])
    else:
        raise ValueError("Letter %s couldn't be encoded to vector" %letter)
 
def vectorToLetter(vector):
#    if not isinstance(vector,(np.ndarray,list)):
#        raise TypeError("Vector should be np.ndarray (or eq), %s (%s) given"
#                        %(vector, type(vector)))
    if np.array_equal(vector,[1,0,0,0]):
        return "u"
    elif np.array_equal(vector,[0,1,0,0]):
        return "r"
    elif np.array_equal(vector,[0,0,1,0]):
        return "d"
    elif np.array_equal(vector,[0,0,0,1]):
        return "l"
    else:
        raise ValueError("Vector %s couldn't be decoded to letter" %vector)

def numToLetter(number):
    if number == 0:
        return "u"
    elif number == 1:
        return "r"
    elif number == 2:
        return "d"
    elif number == 3:
        return "l"
    else:
        raise ValueError("Number %s couldn't be translated to letter" %number)

def numToVector(number):
    if number == 0:
        return oneHotVector("u")
    elif number == 1:
        return oneHotVector("r")
    elif number == 2:
        return oneHotVector("d")
    elif number == 3:
        return oneHotVector("l")
    else:
        raise ValueError("Number %s couldn't be translated to vector" %number)
    
def mapLetterToPosition(old,letter,inc=1):
    new = None
    if letter == "u":
        new = old[0] - inc, old[1]
    elif letter == "d":
        new = old[0] + inc, old[1]
    elif letter == "l":
        new = old[0], old[1] - inc
    elif letter == "r":
        new = old[0], old[1] + inc
    return new
    
def getOppositeDir(letter):
    if letter == "d":
        return "u"
    elif letter == "u":
        return "d"
    elif letter == "l":
        return "r"
    elif letter == "r":
        return "l"