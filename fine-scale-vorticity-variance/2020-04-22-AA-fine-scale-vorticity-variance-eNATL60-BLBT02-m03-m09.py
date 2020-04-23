#!/usr/bin/env python

#import dask
#import dask.threaded
#import dask.multiprocessing
#from dask.distributed import Client

#c = Client()
#c


## path for mdules

import sys
sys.path.insert(0,"/scratch/cnt0024/hmg2840/albert7a/DEV/git/xscale")
import xscale

sys.path.insert(0,"/scratch/cnt0024/hmg2840/albert7a/DEV/git/diags-CMEMS-on-occigen/common-lib/")
import GriddedData

## imports

import numpy as np
import numpy.ma as ma
import xarray as xr
import time

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import matplotlib.cm as mplcm
seq_cmap = mplcm.Blues
div_cmap = mplcm.seismic

### quick plot
import matplotlib.pyplot as plt

import glob
import os 


config='eNATL60'
case='BLBT02'



## Dataset

gridfile='/store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-I/coordinates_eNATL60.nc'
maskfile='/store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-I/mesh_mask_eNATL60_3.6.nc'
meshhgrfile='/store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-I/mesh_mask_eNATL60_3.6.nc'
meshzgrfile='/store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-I/mesh_mask_eNATL60_3.6.nc'



grid=xr.open_dataset(gridfile,chunks={'y':700,'x':1000})
navlat= grid['nav_lat']
navlon= grid['nav_lon']
mesh=xr.open_dataset(maskfile,chunks={'y':700,'x':1000})
e1u=mesh.e1u[0]
e1v=mesh.e1v[0]
e2u=mesh.e2u[0]
e2v=mesh.e2v[0]
ff=mesh.ff[0]


def filt(w):
    win_box2D = w.window
    win_box2D.set(window='hanning', cutoff=90, dim=['x', 'y'], n=[90, 90])
    bw = win_box2D.boundary_weights(drop_dims=[])
    w_LS = win_box2D.convolve(weights=bw)
    w_SS=w-w_LS
    return w_SS



def curl(u,v,e1v,e2u,ff):
    '''
    This routine computes the relative vorticity from 2D fields of horizontal velocities and the spatial Coriolis parameter.
    '''
    #Computation of dy(u)
    fe2u=1/e2u
    fse2u=fe2u.squeeze()
    dyu=(u.shift(y=-1) - u)*fse2u
    #Computation of dx(v)
    fe1v=1/e1v
    fse1v=fe1v.squeeze()
    dxv=(v.shift(x=-1) - v)*fse1v
    #Projection on the grid T
    dxvt=0.5*(dxv.shift(y=-1)+dxv)
    dyut=0.5*(dyu.shift(x=-1)+dyu)
    #Computation of the vorticity divided by f
    fff=1/ff
    curl=(dxvt-dyut)*fff
    return curl


def plot_fine_scale_variance(var,loncrs,latcrs,lon,lat,hpvarm,month,m,config,case):
    ''' map of the averaged fine scale variance
    '''
    fig, ax = plt.subplots(1,1,figsize=(15,10))
    ax = plt.subplot(111,projection=ccrs.PlateCarree(central_longitude=0))
    ax.autoscale(tight=True)
    cont=np.isnan(hpvarm)
    gl = ax.gridlines(draw_labels=True, linestyle=':', color='black',
                      alpha=0.5)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size': 25, 'color': 'gray'}
    gl.ylabel_style = {'size': 25, 'color': 'gray'}
    
    ax.tick_params('both',labelsize=25)

    pcolor = ax.pcolormesh(loncrs,latcrs,ma.masked_invalid(var),cmap=seq_cmap,vmin=0,vmax=0.1,alpha=1)
    ax.contour(lon,lat,cont,alpha=0.5,linewidth=0.000001,antialiased=True,colors='black')
    cbar = plt.colorbar(pcolor,orientation='horizontal',pad=0.1)
    cbar.ax.tick_params(labelsize=25)
    cbar.set_label('Small scales surface vorticity variance in '+month+' for '+config+'-'+case,fontsize=15)
    plt.savefig(config+'-'+case+'_y'+year+'m'+m+'_fine_scale_variance_vorticity.png')
  



def plot_vorticity_variance(month):
    datadir='/store/CT1/hmg2840/lbrodeau/'+str(config)+'/'+str(config)+'-'+str(case)+'*-S/'
    filesU=datadir+'*/'+str(config)+'-'+str(case)+'*_1h_*_gridU-2D_2009'+str(month)+'??-2009'+str(month)+'??.nc'
    filesV=datadir+'*/'+str(config)+'-'+str(case)+'*_1h_*_gridV-2D_2009'+str(month)+'??-2009'+str(month)+'??.nc'
    dsu=xr.open_mfdataset(filesU,chunks={'time_counter':1,'y':700,'x':1000})
    dsv=xr.open_mfdataset(filesV,chunks={'time_counter':1,'y':700,'x':1000})
    u=dsu.sozocrtx
    v=dsv.somecrty
    curl=curl(u,v,e1v,e2u,ff)
    curl_SS=filt(curl)
    curl_LS=curl-curl_SS
    hpcurl=curl_SS
    hpcurl2 = hpcurl ** 2
    hpcurl2m = hpcurl2.mean(axis=0,keep_attrs=True)
    navlat2=np.array(navlat).squeeze()
    navlon2=np.array(navlon).squeeze()
    mgrd = GriddedData.grid2D(navlat=navlat2, navlon=navlon2)
    crs = GriddedData.grdCoarsener(mgrd,crs_factor=60)
    hpcurl2mc = crs.return_ravel(np.asarray(hpcurl2m))
    hpcurl2mcm = np.mean(hpcurl2mc,axis=-3)
    latcrs=crs.return_ravel(np.asarray(navlat2))
    loncrs=crs.return_ravel(np.asarray(navlon2))
    latcrsm=np.mean(latcrs,axis=-3)
    loncrsm=np.mean(loncrs,axis=-3)
    if month == '03':
        plot_fine_scale_variance(hpcurl2mcm,loncrsm, latcrsm,navlon,navlat,hpcurl2m,'March',month,config,case)
    if month == '09':
        plot_fine_scale_variance(hpcurl2mcm,loncrsm, latcrsm,navlon,navlat,hpcurl2m,'September',month,config,case)
        


month_list=['03','09']

for month in month_list:
    plot_vorticity_variance(month)

