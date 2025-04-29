import numpy as np
from photon import photon
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import seaborn as sns
x0 = 0
y0 = 0
theta0 = 0
g = 0.85
pos = 50
nphotons = 10**3
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
    xi = np.random.uniform(0, 1, size)
    if g == 0:
        cos_theta = 2*xi-1
    else:
        num = 1-g**2
        denom = 1-g+2*g*xi
        cos_theta = (1+g**2-(num/denom)**2)/(2*g)

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
        obj = photon(x0,y0,theta0)
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

title1 = ['Histogram: 25m Scattering 1000m Absorption', 
         'Histogram: 15m Scattering 1000m Absorption', 
         'Histogram: 5m Scattering 1000m Absorption']

title2 = ['Histogram: 10m Scattering 50m Absorption', 
         'Histogram: 10m Scattering 150m Absorpotion', 
         'Histogram: 10m Scattering 15000 Absorption']


fig, axs = plt.subplots(len(out_al), 2, figsize=(12, 4 * len(out_al)))

for o, i in enumerate(out_al):
    # Count histogram
    axs[o, 0].hist(i, bins=61, alpha=0.75, color=colors[o], edgecolor='black')
    axs[o, 0].set_title(f'{title2[o]} - Count Histogram')

    # Density histogram
    sns.histplot(i, bins=61, stat='density', ax=axs[o, 1],
                 color=colors[o], edgecolor='black', alpha=0.75)

    # KDE overlay in red
    sns.kdeplot(i, ax=axs[o, 1], color='red', linewidth=2)

    axs[o, 1].set_title(f'{title2[o]} - Density + KDE')

plt.tight_layout()
plt.savefig('VariedAbsorption.pdf')
plt.show()


fig, axs = plt.subplots(len(out_sl), 2, figsize=(12, 4 * len(out_sl)))

for o, i in enumerate(out_sl):
    # Count histogram
    axs[o, 0].hist(i, bins=61, alpha=0.75, color=colors[o], edgecolor='black')
    axs[o, 0].set_title(f'{title1[o]} - Count Histogram')

    # Density histogram
    sns.histplot(i, bins=61, stat='density', ax=axs[o, 1],
                 color=colors[o], edgecolor='black', alpha=0.75)

    # KDE overlay in red
    sns.kdeplot(i, ax=axs[o, 1], color='red', linewidth=2)

    axs[o, 1].set_title(f'{title1[o]} - Density + KDE')

plt.tight_layout()
plt.savefig('VariedScattering.pdf')
plt.show()
