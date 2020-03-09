#!/bin/ksh
#SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --mem=64Gb
#SBATCH --constraint=HSW24
#SBATCH -J make_tide
#SBATCH -e make_tide.e%j
#SBATCH -o make_tide.o%j
#SBATCH --time=1:59:00
#SBATCH --exclusive

CONFIG=eNATL60
CASE=BLBT02

dateini=y2009m06d30
datefin=y2010m10d29

freq=1h

year=$(echo $dateini | awk -Fy '{print $2}' | awk -Fm '{print $1}')
m1=$(echo $dateini | awk -Fm '{print $2}' | awk -Fd '{print $1}')
m2=$(echo $datefin | awk -Fm '{print $2}' | awk -Fd '{print $1}')
d1=$(echo $dateini | awk -Fd '{print $2}')
d2=$(echo $datefin | awk -Fd '{print $2}')


mkdir -p /scratch/cnt0024/hmg2840/albert7a/eNATL60/eNATL60-BLBT02-S/1h/tide

cd /scratch/cnt0024/hmg2840/albert7a/eNATL60/eNATL60-BLBT02-S/1h/tide

for month in $(seq $m1 $m2); do

  mm=$(printf "%02d" $month)

  case $month in
 
    $m1) for day in $(seq $d1 31); do
           dd=$(printf "%02d" $day)
	   ln -sf /store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-BLBT02*-S/*/eNATL60-BLBT02*_1h_*_gridT-2D_${year}${mm}${dd}-${year}${mm}${dd}.nc .
         done;;
    $m2) for day in $(seq 1 $d2); do
           dd=$(printf "%02d" $day)
	   ln -sf /store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-BLBT02*-S/*/eNATL60-BLBT02*_1h_*_gridT-2D_${year}${mm}${dd}-${year}${mm}${dd}.nc .
         done;;

    *) for day in $(seq 1 31); do
           dd=$(printf "%02d" $day)
	   ln -sf /store/CT1/hmg2840/lbrodeau/eNATL60/eNATL60-BLBT02*-S/*/eNATL60-BLBT02*_1h_*_gridT-2D_${year}${mm}${dd}-${year}${mm}${dd}.nc .
         done;;

  esac

done

for file in $(ls *gridT-2D*.nc); do
  if [ ! -e "$file" ]; then
    rm $file
  fi
done

ln -sf /scratch/cnt0024/hmg2840/albert7a/DEV/git/eNATL60-plots-paper/amp-phase-tides-FES/namelist_tideharm namelist

/scratch/cnt0024/hmg2840/albert7a/DEV/git/TIDAL_TOOLS/bin/tid_harm_ana -l *gridT-2D*nc
