import numpy as np
import matplotlib.pyplot as plt

class photon:
    def __init__(self, x, y, angle,energy):
        self.x = x  # Position (x)
        self.y = y  # Position (y)
        self.angle = angle  # Direction of travel
        self.path = [[x, y]]  # List to store the photon’s path
        self.energy = energy
        self.alive = True  # State: True means photon is still in the medium

    def move(self, step_size):
        dx = float(step_size * np.cos(self.angle))
        dy = float(step_size * np.sin(self.angle))
        self.x += dx
        self.y += dy
        self.path.append([self.x, self.y])

    def absorb(self,energy_loss):
        self.energy -= energy_loss

    def scatter(self,angle):
        self.angle += angle

