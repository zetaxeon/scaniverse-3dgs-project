# Data

The large point-cloud scans are **not** stored in this repository (each `.ply` is
100 MB+). Download / copy them yourself and place them here:

```
data/
└─ raw/
   ├─ low.ply      # camera ≈ 30 cm
   ├─ middle.ply   # camera ≈ 60 cm
   └─ high.ply     # camera ≈ 100 cm
```

## About the scans
- Three 3D Gaussian Splatting reconstructions (exported as PLY from **Scaniverse**)
  of the **same** wet-road scene: a puddle with a can beside it.
- Only the **camera height** differs between scans (~30 / 60 / 100 cm).
- Each PLY includes standard 3DGS per-point attributes
  (`x,y,z`, `f_dc_*`, `f_rest_*`, `scale_*`, `opacity`, …).

## Note on coordinate frames
Each Scaniverse export has its **own, independent** coordinate frame and scale.
Do not assume a shared origin or ROI center across scans — the notebook's
sanity-check cell exists to verify scale/extent and to set a per-scan
`ROI_CENTERS` value before comparing.
