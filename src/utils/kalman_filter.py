"""
Description
-----------
Simple Implementation of the Kalman Filter for 1D data, without any dependencies
Originally written in JavaScript by Wouter Bulten
Now rewritten in Python
License
-------
MIT License
2017
Author
------
Sifan Ye
See
---
https://github.com/wouterbulten/kalmanjs
    
"""

import numpy as np
import matplotlib.pyplot as plt

class KalmanFilter:

    cov = float('nan')
    x = float('nan')

    def __init__(self, R, Q):
        """
        Constructor
        :param R: Process Noise
        :param Q: Measurement Noise
        """
        self.A = 1
        self.B = 0
        self.C = 1

        self.R = R
        self.Q = Q

    def kalman_filter(self, measurement):
        """
        Filters a measurement
        :param measurement: The measurement value to be filtered
        :return: The filtered value
        """
        u = 0
        if np.isnan(self.x):
            self.x = (1 / self.C) * measurement
            self.cov = (1 / self.C) * self.Q * (1 / self.C)
        else:
            predX = (self.A * self.x) + (self.B * u)
            predCov = ((self.A * self.cov) * self.A) + self.R

            # Kalman Gain
            K = predCov * self.C * (1 / ((self.C * predCov * self.C) + self.Q))

            # Correction
            self.x = predX + K * (measurement - (self.C * predX))
            self.cov = predCov - (K * self.C * predCov)

        return self.x

    def last_measurement(self):
        """
        Returns the last measurement fed into the filter
        :return: The last measurement fed into the filter
        """
        return self.x

    def set_measurement_noise(self, noise):
        """
        Sets measurement noise
        :param noise: The new measurement noise
        """
        self.Q = noise

    def set_process_noise(self, noise):
        """
        Sets process noise
        :param noise: The new process noise
        """
        self.R = noise

if __name__ == "__main__":
    print("\nRunning script as a demo ...\n")

    # Instanciate Kalman Filter
    process_noise = 1.0 # Default : 0.008
    measurement_noise = 0.1 # Default : 0.1
    kf = KalmanFilter(process_noise, measurement_noise)
    
    # Create Random Values
    np.random.seed(123)
    num_timesteps = 100
    velocities = np.random.normal(loc=0, scale=0.2, size=num_timesteps)

    # Calculate Raw and Filtered Data
    rawData = np.cumsum(velocities)
    meanRawData = np.full(len(rawData), np.mean(rawData))
    filteredData = np.array([kf.kalman_filter(raw) for raw in rawData])
    meanFilteredData = np.full(len(filteredData), np.mean(filteredData))

    # Plot Results
    plt.plot(rawData, label='Raw Data')
    plt.plot(filteredData, label='Kalman Filtered Data')
    #plt.plot(meanRawData, label='Mean of raw')
    #plt.plot(meanFilteredData, label='Mean of filtered')

    # Add labels and title to the plot
    plt.xlabel('Data Index')
    plt.ylabel('Data Value')
    plt.title(f'Raw vs Filtered Position Measurements\nProcess Noise : {process_noise}\nMeasurement Noise : {measurement_noise}')

    # Show Legend and Plot
    plt.legend()
    plt.show()