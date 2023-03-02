import numpy as np
from scipy.stats import norm

# Define motion model
def motion_model(particles, u, std):
    # Add Gaussian noise to each particle based on motion model
    new_particles = np.zeros_like(particles)
    for i in range(particles.shape[0]):
        new_particles[i] = np.random.normal(particles[i] + u, std)
    return new_particles

# Define measurement model
def measurement_model(particles, measurements, std, beacons):
    # Calculate likelihood of each particle based on RSSI measurements
    weights = np.zeros(particles.shape[0])
    for i in range(particles.shape[0]):
        predicted_measurements = np.array([calculate_RSSI(particles[i], beacon) for beacon in beacons])
        likelihoods = norm.pdf(measurements, loc=predicted_measurements, scale=std)
        weights[i] = np.prod(likelihoods)
    return weights / np.sum(weights)

# Define resampling function
def resampling(particles, weights):
    # Resample particles based on their weights
    indices = np.random.choice(range(particles.shape[0]), size=particles.shape[0], p=weights)
    new_particles = particles[indices]
    new_weights = np.ones_like(weights) / particles.shape[0]
    return new_particles, new_weights

# Define function to calculate RSSI values from location
def calculate_RSSI(location, beacon):
    A = -69.5 # RSSI at 1m
    n = 2.7 # Path-loss exponent
    distance = np.sqrt((location[0] - beacon[0])**2 + (location[1] - beacon[1])**2)
    return A - 10 * n * np.log10(distance)

# Define main function to run particle filter
def particle_filter(measurements, beacons, num_particles=1000, std_motion=0.1, std_measurement=2):
    print("STARTING PARTICLE FILTERING...")

    # Initialize particles
    particles = np.random.uniform(low=0, high=10, size=(num_particles, 2))
    weights = np.ones_like(particles) / num_particles

    # Iterate over measurements
    for i in range(len(measurements)):
        # Predict next state of each particle
        particles = motion_model(particles, u=[0.1, 0.1], std=std_motion)

        # Update weights based on measurements
        weights = measurement_model(particles, measurements[i], std=std_measurement, beacons=beacons)

        # Resample particles
        particles, weights = resampling(particles, weights)

    # Estimate user's location
    estimated_location = np.average(particles, axis=0, weights=weights)
    
    print("DONE PARTICLE FILTERING.")
    return estimated_location

## Where :
## measurements = [beacon1_RSSI, beacon2_RSSI, beacon3_RSSI]
## beacons = [(1, 2), (4, 5), (3, 1)]
## estimated_location = particle_filter(measurements, beacons)

