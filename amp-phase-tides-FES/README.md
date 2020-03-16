## Requisite
The harmonic analysis of the eNATL60 outputs needs :

  - the `TIDAL_TOOLS` :  https://github.com/molines/TIDAL_TOOLS
  - the python script made by Laurent : `cal1:/mnt/meom/workdir/brodeau/DEV/nemo_conf_manager/misc/pythontidal_cplx_to_amp.py`

## Steps
  - the harmonic analysis is performed by submitting a job to visu (large memory needed) : script `make_tidal_amp_phase.ksh`
  - the `x_elev`, `y_elev` outputs for each frequency are transformed into amplitude and phase : 
  - the plots are produced :
