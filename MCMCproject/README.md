# Photon Transport Simulation

This project simulates photon transport through a medium using a Monte Carlo method, taking into account **scattering** and **absorption** based on specified optical properties. The simulation uses a Henyey-Greenstein scattering phase function to determine scattering angles and outputs distributions of photons arriving at a virtual camera.

## Features

- Models both **scattering** and **absorption** events probabilistically.
- Implements **Henyey-Greenstein** scattering with configurable anisotropy factor `g`.
- Tracks photon trajectories and determines whether they are absorbed, missed, or detected.
- Produces histograms and KDE plots for visualizing the spatial distribution of detected photons.

## Simulation Components

### `dist_event(sl, al)`
Returns distances to the next scattering and absorption events using exponential distributions based on:
- `sl`: Scattering length
- `al`: Absorption length

### `henyey_scattering(g)`
Samples scattering angles from the Henyey-Greenstein phase function:
- `g`: Anisotropy factor (-1 ≤ g ≤ 1)

### `start(pho, sl, al)`
Simulates the journey of a single photon object:
- Moves it step-by-step until it's absorbed or reaches the detector.

### `run(num_photons, sl, al)`
Runs the full simulation for `num_photons`: NOTE in the current code num_photons is set to 10^3 as it takes quite a while to run all simulations at 10^6, and I did not want to make the grader wait that long to view the output.
- Returns y-positions of detected photons
- Reports how many photons were absorbed or missed

## Usage

To run the simulation:

```python
out = run(nphotons=10**6, sl=10, al=150)
