# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 18:57:58 2018

@author: Xiaosong Zhu
"""


import sys
sys.path.append('/bigwork/nhbbzhux/Tools/mypip/lib/python3.5/site-packages')

from fproj import fproj

########### Input ###########
str_nstate_left = input('Input the number of the state you on the left side: ')
str_nstate_right = input('Input the number of the state you on the right side: ')

# number of atom 
natom = input('Input the number of atoms (Directly press Enter for 1): ')
if natom=='':
    natom='1'
natom = int(natom)

# step of temperal grid
ntstep = input('Input the step of the temporal grid (Press ENTER for 50): ')
if ntstep=='':
    ntstep='50'
ntstep = int(ntstep)

# dt
dt = float(input('Input the value of dt: '))

# max temeral grid
maxnt = int(input('Input the max temeral grid to be read: '))


########## main ##########
fproj(str_nstate_left,str_nstate_right,natom,ntstep,dt,maxnt)
