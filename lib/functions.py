# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:19:06 2020

@author: jimen
"""
import values

def mtopx(dinm):
    ''' Convertit les distances en m vers des pixels'''
    return int(dinm*values.PXPM)

def OMtopx(OM):
    '''Convertit les positions en m vers des coords en pixels
       Retourne un tuple '''
    return (mtopx(OM[0])+values.XSHIFT,values.YMAX-mtopx(OM[1]))

def norm(vect):
    return vect.length()