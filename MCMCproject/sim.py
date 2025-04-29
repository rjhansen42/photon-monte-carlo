import numpy as np
from photon import photon
import matplotlib.animation as animation
import matplotlib.pyplot as plt

scattering_length = 5
absoprtion_length = 1000
x0 = 0
y0 = 0
e0=1
theta0 = 0
g = 0.85
pos = 50
nphotons = 10**5
cam_size = 50

def dist_event(sl, al): #Based on exponential distribution with params scattering and absorption length
    rs = 1/sl
    ra = 1/al
    us = np.random.rand()
    while us == 0:          # This is to prevent the edge case where u = 0, which would cause the ln(u) to be undefined.
        us = np.random.rand()
    ua = np.random.rand()
    while ua == 0:          # This is to prevent the edge case where u = 0, whaich would cause the ln(u) to be undefined.
        ua = np.random.rand()
    
    xs = -np.log(1-us)/rs #dist to scattering event
    xa = -np.log(1-ua)/ra #dist to absorption event

    return [xs,xa]

def henyey_scattering(g, size=1, return_cos=False): #Simulates angle using henyey greenstein scattering function
    """
    Sample scattering angles from the Henyey-Greenstein phase function.
    Parameters:
    - g (float): Anisotropy factor (-1 to 1). g = 0 is isotropic.
    - size (int): Number of samples to generate.
    - return_cos (bool): If True, return cos(theta) instead of theta in radians.
    Returns:
    - ndarray: Array of angles in radians or cos(theta) values.
    """
    xi = np.random.uniform(0, 1, size)
    if g == 0:
        cos_theta = 2 * xi - 1
    else:
        num = 1 - g**2
        denom = 1 - g + 2 * g * xi
        cos_theta = (1 + g**2 - (num / denom)**2) / (2 * g)

    theta = np.arccos(cos_theta)
    if np.random.rand() < 0.5:        # Without this addition angle is always positive
        theta = -theta
    return theta

def start(pho, sl, al): #Calls dist_event and henyey to actively run simulation
    temp, abs_dist = dist_event(sl,al)
    s=0
    while abs(pho.x) < pos:            
        step = dist_event(sl, al)
        scatter_dist = step[0]
        pho.move(scatter_dist)
        if pho.x > pos:
            x0, y0 = pho.path[-2]
            x1 = pos
            y1 = y0 + np.tan(pho.angle)*(x1-x0)
            pho.path[-1] = [x1, y1]
        pho.scatter(henyey_scattering(g))
        for i in range(len(pho.path)-1):
            coord = pho.path
            s += np.sqrt((coord[i+1][0]-coord[i][0])**2+(coord[i+1][1]-coord[i][1])**2)
            if s >= abs_dist:
                pho.path[-1] = ['Absorbed', 'Absorbed']
                return pho
    return pho

def run(num_photons, sl, al): #Generates photon objects and feeds them into start to run simulation
    photons = []
    y = []
    miss_counter = 0
    abs_counter = 0
    for i in range(num_photons):
        obj = photon(x0,y0,theta0,e0)
        start(obj, sl, al)
        photons.append(obj)

    for i, pho in enumerate(photons):
        yf = pho.path[-1][1]
        if isinstance(yf, str) == True:
            abs_counter += 1
        elif np.abs(yf) < cam_size:
            if isinstance(yf, np.ndarray):
                y.append(float(yf[0]))  # or yf.item() if it's a 0-D array
            else:
                y.append(float(yf))  # already a float (or something convertible to float)
        elif np.abs(yf) >= cam_size:
            miss_counter += 1
    out = np.sort(y)
    print('Total Misses: '+str(miss_counter))
    print('Total Absorbed: '+str(abs_counter))
    return out
colors = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:brown",
    "tab:pink",
    "tab:gray",
    "tab:olive",
    "tab:cyan"
]


out_s5_al1000 = run(nphotons, 5, 1000)
out_sl5_al1000 = run(nphotons, 15, 1000)
out_sl25_al1000 = run(nphotons, 25, 1000)
out_sl = [out_sl25_al1000, out_sl5_al1000, out_s5_al1000]

out_sl10_al50 = run(nphotons, 10, 50)
out_sl10_al150 = run(nphotons, 10, 150)
out_sl10_al1500 = run(nphotons, 10, 15000)
out_al = [out_sl10_al50, out_sl10_al150, out_sl10_al1500]

title = ['Histogram: 25m Scattering', 'Histogram: 15m Scattering', 'Histogram: 5m Scattering']

for o, i in enumerate(out_sl):
    plt.hist(i, bins=61, alpha = 0.5, color=colors[o],edgecolor='black')
    plt.title(title[o])
plt.show()

for o, i in enumerate(out_al):
    plt.hist(i, bins=61, alpha = 0.8, color=colors[o],edgecolor='black')
plt.show()

