# Photon Transport Simulation

This project simulates photon transport through a medium using a Monte Carlo method, taking into account **scattering** and **absorption** based on specified optical properties. The simulation uses a Henyey-Greenstein scattering phase function to determine scattering angles and outputs distributions of photons arriving at a virtual camera.

I do research as part of the CamSim group with Carsten Rott, and much of my working involves running simulatiosn of this sort on super computers. Of course the simulation code used in IceCube's CamSim group are much more nuanced and complicated, I recreated it using the same henyey scattering function and I am very pleased with the result. I have gained a much better understanding of how Monte Carlo sampling works and is used, as well as how photons are simulated. Additionally, my resulting graphs are very simialr to the ones made using the official PPC code from IceCube.

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
