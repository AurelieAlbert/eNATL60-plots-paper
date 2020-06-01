
for file in maps_amp_phi_K1_eNATL60_pytide.png maps_amp_phi_M2_eNATL60_pytide.png maps_amp_phi_N2_eNATL60_pytide.png maps_amp_phi_O1_eNATL60_pytide.png maps_amp_phi_S2_eNATL60_pytide.png maps_amp_phi_K1_eNATL60_tidal-tools.png maps_amp_phi_M2_eNATL60_tidal-tools.png maps_amp_phi_N2_eNATL60_tidal-tools.png maps_amp_phi_O1_eNATL60_tidal-tools.png maps_amp_phi_S2_eNATL60_tidal-tools.png; do
    convert $file -trim -bordercolor White -border 20x10 +repage $file
done

montage maps_amp_phi_M2_eNATL60_tidal-tools.png maps_amp_phi_M2_eNATL60_pytide.png maps_amp_phi_S2_eNATL60_tidal-tools.png maps_amp_phi_S2_eNATL60_pytide.png maps_amp_phi_N2_eNATL60_tidal-tools.png maps_amp_phi_N2_eNATL60_pytide.png maps_amp_phi_O1_eNATL60_tidal-tools.png maps_amp_phi_O1_eNATL60_pytide.png maps_amp_phi_K1_eNATL60_tidal-tools.png maps_amp_phi_K1_eNATL60_pytide.png -geometry 800x700 -tile 2x5 -quality 100 maps_amp_phi_M2-S2-N2-O1-K1_eNATL60_tidal-tools-pytide.png

convert maps_amp_phi_M2-S2-N2-O1-K1_eNATL60_tidal-tools-pytide.png -trim -bordercolor White -border 20x10 +repage maps_amp_phi_M2-S2-N2-O1-K1_eNATL60_tidal-tools-pytide.png


