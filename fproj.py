# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 20:10:01 2018

@author: Xiaosong Zhu
"""

import sys
sys.path.append('/bigwork/nhbbzhux/Tools/mypip/lib/python3.5/site-packages')

import numpy as np
import linecache
import matplotlib.pyplot as plt

########### Function ###########
def fproj(str_nstate_left,str_nstate_right,natom,ntstep,dt,maxnt):   
    
    ##### the state to be read on the left side #####  
    str_temp = 'wf-st'+'0'*(4-len(str_nstate_left))+str_nstate_left
    filename_real_left = str_temp+'.real.xsf'
    filename_imag_left = str_temp+'.imag.xsf'
    print('So the files to be read are: \n',filename_real_left,filename_imag_left,'\n')
    
    ##### the state to be read on the right side #####
    str_temp = 'wf-st'+'0'*(4-len(str_nstate_left))+str_nstate_right
    filename_real_right = str_temp+'.real.xsf'
    filename_imag_right = str_temp+'.imag.xsf'
    print('So the files to be read are: \n',filename_real_right,filename_imag_right,'\n')
    
    ##### prepare to read data #####    
    begin_gridinfo = 5+natom       # the grid information begins from this line  (Line number starts from 1!)
    begin_data = 10+natom    # the data begins from this line (Line number starts from 0!)
    
    ##### Read the spatial grid  #####
    td0000000 = 'td.0000000'
    print('Read the spatial grid and inital state from',td0000000,'...')
    
    pathfile = './'+td0000000+'/'+filename_real_left
    
    # with open(pathfile, "r") as f:
    print('Open',pathfile)
    
    # number of grids, like  "101    121     81"
    head0 = linecache.getline(pathfile,begin_gridinfo)  
    head0 = head0.split()
    Lx = int(head0[0])
    Ly = int(head0[1])
    Lz = int(head0[2])
    print('Lx, Ly, Lz = \n',Lx,Ly,Lz)
    
    # xmax
    head2 = linecache.getline(pathfile,begin_gridinfo+2) 
    head2 = head2.split()
    Rx = float(head2[0])/2          # don't forget /2
    
    # ymax
    head3 = linecache.getline(pathfile,begin_gridinfo+3) 
    head3 = head3.split()
    Ry = float(head3[1])/2
    
    # zmax
    head4 = linecache.getline(pathfile,begin_gridinfo+4) 
    head4 = head4.split()
    Rz = float(head4[2])/2
    
    print('Rx, Ry, Rz = \n',Rx,Ry,Rz)
    
    dx = 2*Rx/(Lx-1)
    dy = 2*Ry/(Ly-1)
    dz = 2*Rz/(Lz-1)
    print('dx, dy, dz = \n',dx,dy,dz,'\n')    
    
    # real part of the inital state
    real_vec = np.loadtxt(pathfile,skiprows=begin_data-1,dtype=bytes)  # ??!!
    real_vec = real_vec[:-2].astype(float)		# remove the last two non-data lines
    
    # imag part of the inital state
    pathfile = './'+td0000000+'/'+filename_imag_left
    print('Read',pathfile)
    
    imag_vec = np.loadtxt(pathfile,skiprows=begin_data-1,dtype=bytes)
    imag_vec = imag_vec[:-2].astype(float)			
    
    vec0 = real_vec + 1j*imag_vec
    
    norm = np.sum( np.abs(vec0) * np.abs(vec0) )*dx*dy*dz
    print('The norm of the inital state is',norm,'\n')
        
        
    ##### read td files and calcualte the td-proj #####
    
    # parepare for td
    temp_t=0
    t = []
    proj = []
    
    for n in range(0, maxnt+ntstep, ntstep):
        
        print('t=',temp_t)
        
        # read orbital
        str_n = str(n)
        str_folder = 'td.'+'0'*(7-len(str_n))+str_n
        
            # real part
        pathfile = './'+str_folder+'/'+filename_real_right
        print('read',pathfile)
        real_vec = np.loadtxt(pathfile,skiprows=begin_data-1,dtype=bytes)
        real_vec = real_vec[:-2].astype(float)
        
            # real part
        pathfile = './'+str_folder+'/'+filename_imag_right
        print('read',pathfile)
        imag_vec = np.loadtxt(pathfile,skiprows=begin_data-1,dtype=bytes)
        imag_vec = imag_vec[:-2].astype(float)
    
        vect = real_vec + 1j*imag_vec
        norm = np.sum( np.abs(vec0) * np.abs(vec0) )*dx*dy*dz
        print('norm=',norm,'\n')
        
        # calculate
        temp_proj = np.sum( np.conj(vec0) * vect )*dx*dy*dz
        
        t.append(temp_t)
        proj.append(temp_proj)
        
        # next
        temp_t = temp_t + dt*ntstep
        
    ##### save the data #####
    save_vorname = 'proj'+str_nstate_right+'to'+str_nstate_left
    savefile=save_vorname+'.txt'
    np.savetxt(savefile,np.column_stack( (t,np.real(proj),np.imag(proj)) ))
    
    ##### plot #####
    line1,=plt.plot(t,np.real(proj),label='real')
    line2,=plt.plot(t,np.imag(proj),label='imag')
    line3,=plt.plot(t,np.abs(proj),label='abs')

    plt.legend(loc='upper right')
    plt.title(save_vorname)  
    plt.xlabel('time /a.u.', fontsize=12, fontweight='bold')
    plt.ylabel('projection', fontsize=12, fontweight='bold')
    
    plt.savefig(save_vorname+'.png',dpi=150,bbox_inches='tight')
    plt.close()
