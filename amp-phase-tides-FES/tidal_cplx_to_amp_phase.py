#!/usr/bin/env python

#       B a r a K u d a
#
#  Prepare 2D maps (monthly) that will later become a GIF animation!
#  NEMO output and observations needed
#
#    L. Brodeau, May 2018

import sys
import os
import numpy as nmp
from netCDF4 import Dataset
import warnings
warnings.filterwarnings("ignore")

import barakuda_tool as bt
import barakuda_ncio as bnc

#l_debug = True

cextra = ''


narg = len(sys.argv)
if not narg in (5,6):
    print('Usage: '+sys.argv[0]+' <Constituent_file> <name_Real_part>  <name_Imaginary_part> <iconjug (conjugate? 0=no,1=yes)> (<extra_info_like_constituend_name>)')
    sys.exit(0)
cf_in = sys.argv[1]
cv_re = sys.argv[2]
cv_im = sys.argv[3]
cv_cj = sys.argv[4] ; iconj = int(cv_cj)

if narg==6: cextra = sys.argv[5]+'_'

cf_out = cextra+cf_in.replace('.nc','_AP.nc')


#============================================
id_in = Dataset(cf_in)


cv_lon = ''
cv_lat = ''
list_var = id_in.variables.keys()
for cv in list_var:
    if 'lon' in cv: cv_lon = cv
    if 'lat' in cv: cv_lat = cv




    
if cv_lon != '' and cv_lat != '':
    l_coor = True
    print(' *** Will use variable "'+cv_lon+'" for longitude!')
    print(' *** Will use variable "'+cv_lat+'" for latitude!\n')
    
    nb_dim_coor = len(id_in.variables[cv_lon].dimensions)
    if nb_dim_coor==2:
        xlon  = id_in.variables[cv_lon][:,:]
        xlat  = id_in.variables[cv_lat][:,:]
    elif nb_dim_coor==1:
        xlon  = id_in.variables[cv_lon][:]
        xlat  = id_in.variables[cv_lat][:]
    else:
        print('ERROR: unknown number of dimensions for coordinates!!!')
        sys.exit(0)
    
else:
    l_coor = False
    xlon=[]
    xlat=[]


nb_dim_fld = len(id_in.variables[cv_re].dimensions)

if nb_dim_fld==2:
    xre  = id_in.variables[cv_re][:,:]
    xim  = id_in.variables[cv_im][:,:]
elif nb_dim_fld==3:
    xre  = id_in.variables[cv_re][0,:,:]
    xim  = id_in.variables[cv_im][0,:,:]
else:
    print('ERROR: unknown number of dimensions for "'+cv_re+'" !!!', nb_dim_fld)
    sys.exit(0)

id_in.close()



#============================================

print("Everything read!\n")

(ny,nx) = nmp.shape(xre)

print(' => dimension =', nx, ny)

print(' arccos(-1) => ', nmp.arccos(-1.))
print('    Pi    => ', nmp.pi)


zAP = nmp.zeros((2,ny,nx))

# Amplitude:
zAP[0,:,:] = nmp.sqrt(xre[:,:]*xre[:,:] + xim[:,:]*xim[:,:]) # ampl. from Im(z) and Re(z)

# Phase:
zAP[1,:,:] = nmp.arctan2(xim[:,:], xre[:,:]) # phase in radian [-Pi,+Pi] from Im(z) and Re(z)
zAP[1,:,:] = zAP[1,:,:] * 180./nmp.pi        # phase in degrees [-180., 180], not radian
if iconj==1: zAP[1,:,:] = zAP[1,:,:] * -1.0
#zAP[1,:,:] = nmp.mod(zAP[1,:,:], 360.) # [ 0. , 360. ]



bnc.dump_2d_multi_field(cf_out, zAP, ['r','phi'], vndim=[2,2], xlon=xlon, xlat=xlat)


print('')
