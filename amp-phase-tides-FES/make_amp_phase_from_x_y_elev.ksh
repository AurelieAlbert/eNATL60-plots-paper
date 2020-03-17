cd /scratch/cnt0024/hmg2840/albert7a/eNATL60/eNATL60-BLBT02-S/1h/tide/


cp /scratch/cnt0024/hmg2840/albert7a/DEV/git/eNATL60-plots-paper/amp-phase-tides-FES/tidal_cplx_to_amp_phase.py .
cp /scratch/cnt0024/hmg2840/albert7a/DEV/git/eNATL60-plots-paper/amp-phase-tides-FES/barakuda* .

tidal_cplx_to_amp_phase.py res_harm_ssh_0-360.nc M2_x_elev M2_y_elev 1 M2
