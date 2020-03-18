# New strategy for a statistical comparison to EN4 profiles

## Inspiration of previous developments
  - CMEMS diags on NATL60 : https://github.com/auraoupa/CMEMS-diags/tree/master/Comp_ARGO_profiles
  - CMEMS diags on EU and GS : https://github.com/auraoupa/diags-CMEMS-on-occigen/tree/master/Profiles-EN4
  
## Steps

  1. Download 2009 EN4 data : download_EN4-2009_from_ifremer.ksh
  1. Modify selection script to include the list of model files that will be compared to the profil in the json file
  1. Everything with xarray from the beginning
