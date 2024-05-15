import random
import math
import matplotlib.pyplot as plt

def generate_random_points_normal(center, std_dev, num_points):
    random_points = []
    for _ in range(num_points):
        # Generate random offsets following normal distribution
        offset_x = random.gauss(0, std_dev)
        offset_y = random.gauss(0, std_dev)
        
        # Apply offsets to central point
        random_point = (center[0] + offset_x, center[1] + offset_y)
        random_points.append(random_point)
    return random_points

# Example usage
central_point = (0, 0)  # Define your central point
std_dev = 1  # Define the standard deviation
num_points = 1000  # Number of random points to generate
random_points = generate_random_points_normal(central_point, std_dev, num_points)

# Unzip the random points into separate lists for x and y coordinates
x_coords, y_coords = zip(*random_points)

# Plot the random points
plt.figure(figsize=(8, 8))
plt.scatter(x_coords, y_coords, color='blue', s=10, alpha=0.5)
plt.scatter(central_point[0], central_point[1], color='red', marker='x', s=10, label='Central Point')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Random Points Following Normal Distribution')
plt.legend()
plt.grid(True)
plt.axis('equal')  # Equal aspect ratio for better visualization
plt.show()
