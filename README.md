# Camera voltage analysis

### [Voltage analysis](https://github.com/NGTS/analysis-camera-voltages/blob/master/VoltageAnalysis.ipynb)

The initial analysis exploring the saturation levels for the different camera voltages. It shows that changing the voltage towards higher settings (e.g. VI+223) yields a higher saturation limit at little to no cost. *There is still the question of the noise levels of bright non-saturated stars though.*

### [Frame histograms](https://github.com/NGTS/analysis-camera-voltages/blob/master/frame_histograms.ipynb)

A study of histograms of the raw frames for three voltages (chosen to have similar conditions night to night), showing the different saturation points and full well levels.

Towards the bottom is a comparison of the flux levels measured by the pipeline in single images across the three voltage settings. I have not interpreted this yet.

### [Other camera comparison](https://github.com/NGTS/analysis-camera-voltages/blob/master/other_camera_comparison.ipynb)

Can we use other cameras observing the same field to calibrate the camera with a different voltage?

I find that for the bright stars yes we can calibrate, but haven't explored the full flux range required to assess performance. We may have to use the bright stars to calibrate the faint stars in some way.

I tested two cameras with the *same* voltage settings for this test to set a baseline, and find that the two cameras have different [gain/throughput] levels. This may be expected if it's a gain issue. Something to watch for.


## Workbooks still in progress

### [Paladin analysis](https://github.com/NGTS/analysis-camera-voltages/blob/master/paladin_analysis.ipynb)

An attempt to compare cameras just using the output from Paladin.

### [Simultaneous analysis](https://github.com/NGTS/analysis-camera-voltages/blob/master/simultaneous_analysis.ipynb)

An early attempt to compare cameras.
