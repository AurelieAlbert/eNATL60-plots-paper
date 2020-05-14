#!/usr/bin/env python

#import psutil

#net_if_addrs = psutil.net_if_addrs()
#allowed_ifnames = list(net_if_addrs.keys())

#print('allowed interfaces are :',allowed_ifnames)
from dask_mpi import initialize
initialize(interface='ib0:0')

from distributed import Client
client = Client()


print('Currently working with '+str(len(client.scheduler_info()["workers"]))+' workers')





