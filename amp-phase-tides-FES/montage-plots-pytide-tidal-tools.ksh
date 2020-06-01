
for file in maps_amp_phi_K1_eNATL60_pytide.png maps_amp_phi_M2_eNATL60_pytide.png maps_amp_phi_N2_eNATL60_pytide.png maps_amp_phi_O1_eNATL60_pytide.png maps_amp_phi_S2_eNATL60_pytide.png ; do
    convert $file -trim -bordercolor White -border 20x10 +repage $file
done
