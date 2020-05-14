#!/usr/bin/env python

from dask_jobqueue import SLURMCluster 
from dask.distributed import Client 
  
cluster = SLURMCluster(cores=28,name='test-jobqueue',walltime='00:06:00',job_extra=['--constraint=HSW24','--exclusive','--nodes=1'],memory='120GB',interface='enp5s0f0') 
cluster.scale(196)
cluster

from dask.distributed import Client
client = Client(cluster)
client



print('Currently working with '+str(len(client.scheduler_info()["workers"]))+' workers')





