#!/usr/bin/env python


from dask_mpi import initialize
initialize()

from distributed import Client
client = Client()


print('Currently working with '+str(len(client.scheduler_info()["workers"]))+' workers')


## path for mdules
print('Importing librairies')
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


import glob
import os 

config='eNATL60'
case='BLBT02'

## Dataset

gridfile='/store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-I/coordinates_eNATL60.nc'
maskfile='/store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-I/mesh_mask_eNATL60_3.6.nc'
meshhgrfile='/store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-I/mesh_mask_eNATL60_3.6.nc'
meshzgrfile='/store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-I/mesh_mask_eNATL60_3.6.nc'

print('Opening grid files')
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





def compute_vorticity_variance(month):
    print('Start')
    datadir='/store/CT1/hmg2840/lbrodeau/'+str(config)+'/'+str(config)+'-'+str(case)+'*-S/'
    filesU=datadir+'*/'+str(config)+'-'+str(case)+'*_1h_*_gridU-2D_20??'+str(month)+'??-20??'+str(month)+'??.nc'
    filesV=datadir+'*/'+str(config)+'-'+str(case)+'*_1h_*_gridV-2D_20??'+str(month)+'??-20??'+str(month)+'??.nc'
    print('Opening dataset with xarray')
    dsu=xr.open_mfdataset(filesU,combine='by_coords',chunks={'time_counter':1,'y':700,'x':1000})
    dsv=xr.open_mfdataset(filesV,combine='by_coords',chunks={'time_counter':1,'y':700,'x':1000})
    u=dsu.sozocrtx
    v=dsv.somecrty
    print('Computing curl')
    curl_surf=curl(u,v,e1v,e2u,ff)
    print('Filtering curl')
    curl_SS=filt(curl_surf)
    curl_LS=curl_surf-curl_SS
    hpcurl=curl_SS
    hpcurl2 = hpcurl ** 2
    hpcurl2m = hpcurl2.mean(axis=0,keep_attrs=True)
    navlat2=np.array(navlat).squeeze()
    navlon2=np.array(navlon).squeeze()
    print('Coarsening of the grid')
    mgrd = GriddedData.grid2D(navlat=navlat2, navlon=navlon2)
    crs = GriddedData.grdCoarsener(mgrd,crs_factor=60)
    hpcurl2mc = crs.return_ravel(np.asarray(hpcurl2m))
    hpcurl2mcm = np.mean(hpcurl2mc,axis=-3)
    latcrs=crs.return_ravel(np.asarray(navlat2))
    loncrs=crs.return_ravel(np.asarray(navlon2))
    latcrsm=np.mean(latcrs,axis=-3)
    loncrsm=np.mean(loncrs,axis=-3)
    print('Saving to netcdf')
    hpcurl2mcm_dataset=hpcurl2mcm.to_dataset(name='coarse-filt-curl') 
    hpcurl2mcm_dataset['latcrsm']=latcrsm
    hpcurl2mcm_dataset['loncrsm']=loncrsm
    hpcurl2mcm_dataset['hpcurl2m']=hpcurl2m
    try:
      os.mkdir('/scratch/cnt0024/hmg2840/albert7a/'+config+'/'+config+'-'+case+'-S/CURL/') 
    except OSError as error: 
      print(error)
    hpcurl2mcm_dataset.to_netcdf(path='/scratch/cnt0024/hmg2840/albert7a/'+config+'/'+config+'-'+case+'-S/CURL/'+config+'-'+case+'_m'+str(month)+'_coarse-filt-surf-curl.nc',mode='w')

month_list=['03']

for month in month_list:
    plot_vorticity_variance(month)




