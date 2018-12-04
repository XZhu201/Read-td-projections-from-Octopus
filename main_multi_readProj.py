# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 18:57:58 2018

@author: Xiaosong Zhu
"""

import sys
sys.path.append('/bigwork/nhbbzhux/Tools/mypip/lib/python3.5/site-packages')


from multiprocessing import Pool    # Parallel
from fproj import fproj          # import my function

# ---------- Input -----------------
natom = 1                 # Input the number of atoms [int]
ntstep = 50               # Input the step of the temperal grid [int]
dt = 0.06                   # Input the value of dt [float]
maxnt = 200                 # Input the max temporal grid to be read [int]
# ----------------------------------

def fpar(nn):        # this func is defined only to run in parallel
    fproj(str(nn[0]),str(nn[1]),natom,ntstep,dt,maxnt)
    
    
list_nleft = []
list_nright = []
for nleft in [2,3,5]:
    for nright in [2,3,5]:        
        list_nleft.append(nleft)
        list_nright.append(nright)

print('list_nleft=\n',list_nleft)
print('list_nright=\n',list_nright)
        
pool = Pool()
pool.map(fpar,zip(list_nleft,list_nright))  # zip is important for pool.map
pool.close()
