import numpy as np
from scipy.stats import norm

# Exemples d'utilisation :
# measurements = [beacon1_RSSI, beacon2_RSSI, beacon3_RSSI]
# beacons = [(1, 2), (4, 5), (3, 1)]
# estimated_location = ParticleFilter.filter(measurements, beacons)

class ParticleFilter:
    def __init__(self, num_particles=1000, std_motion=0.1, std_measurement=2):
        self.num_particles = num_particles
        self.std_motion = std_motion
        self.std_measurement = std_measurement

    def motion_model(self, particles, u):
        # Add Gaussian noise to each particle based on motion model
        new_particles = np.zeros_like(particles)
        for i in range(particles.shape[0]):
            new_particles[i] = np.random.normal(particles[i] + u, self.std_motion)
        return new_particles

    def measurement_model(self, particles, measurements, beacons):
        # Calculate likelihood of each particle based on RSSI measurements
        weights = np.zeros(particles.shape[0])
        for i in range(particles.shape[0]):
            predicted_measurements = np.array([self.calculate_RSSI(particles[i], beacon) for beacon in beacons])
            likelihoods = norm.pdf(measurements, loc=predicted_measurements, scale=self.std_measurement)
            weights[i] = np.prod(likelihoods)
        return weights / np.sum(weights)

    def resampling(self, particles, weights):
        # Resample particles based on their weights
        indices = np.random.choice(range(particles.shape[0]), size=particles.shape[0], p=weights)
        new_particles = particles[indices]
        new_weights = np.ones_like(weights) / particles.shape[0]
        return new_particles, new_weights

    def calculate_RSSI(self, location, beacon):
        A = -69.5 # RSSI at 1m
        n = 2.7 # Path-loss exponent
        distance = np.sqrt((location[0] - beacon[0])**2 + (location[1] - beacon[1])**2)
        return A - 10 * n * np.log10(distance)

    def filter(self, measurements, beacons):
        print("STARTING PARTICLE FILTERING...")

        # Initialize particles
        particles = np.random.uniform(low=0, high=10, size=(self.num_particles, 2))
        weights = np.ones_like(particles) / self.num_particles

        # Iterate over measurements
        for i in range(len(measurements)):
            # Predict next state of each particle
            particles = self.motion_model(particles, u=[0.1, 0.1])

            # Update weights based on measurements
            weights = self.measurement_model(particles, measurements[i], beacons)

            # Resample particles
            particles, weights = self.resampling(particles, weights)

        # Estimate user's location
        estimated_location = np.average(particles, axis=0, weights=weights)

        print("DONE PARTICLE FILTERING.")
        return estimated_location
