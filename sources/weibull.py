import numpy as np
import matplotlib.pyplot as plt

# Parameters for Weibull distribution (shape and scale for wind speed)
k_wind = 2.0  # Shape parameter for wind speed
c_wind = 5.0  # Scale parameter for wind speed (mean wind speed in m/s)

# Parameters for active power output
cut_in_speed = 3.0  # Cut-in wind speed in m/s
rated_power = 100.0  # Rated power output in kW
cut_out_speed = 25.0  # Cut-out wind speed in m/s

# Generate random samples of wind speeds using Weibull distribution
num_samples = 1000
wind_speeds = c_wind * np.random.weibull(k_wind, num_samples)

# Calculate active power output based on wind speeds
active_power = np.zeros_like(wind_speeds)
active_power[wind_speeds < cut_in_speed] = 0.0
active_power[(wind_speeds >= cut_in_speed) & (wind_speeds <= cut_out_speed)] = (
    rated_power 
    * ((wind_speeds[(wind_speeds >= cut_in_speed) & (wind_speeds <= cut_out_speed)] - cut_in_speed) 
    / (cut_out_speed - cut_in_speed)) ** 3
)

# Plotting the histogram of active power output
plt.figure(figsize=(8, 6))
plt.hist(active_power, bins=30, density=True, alpha=0.7, color='blue', edgecolor='black')

# Plot the theoretical probability density function (PDF) of active power
# For Weibull distribution of wind speeds
x = np.linspace(0, rated_power * 1.2, 100)
pdf_wind = (k_wind / c_wind) * (x / c_wind)**(k_wind - 1) * np.exp(-(x / c_wind)**k_wind)
plt.plot(x, pdf_wind, 'r-', lw=2, label='Weibull Wind Speed PDF')

plt.title('Active Power Output Distribution (Weibull)')
plt.xlabel('Active Power (kW)')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.show()




import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min

# Example power generation data (replace this with your actual data)
# This could be derived from wind speed data and a power curve model
power_data = np.array([0.2, 1.5, 5.0, 10.2, 20.0, 35.5, 50.1, 70.2, 90.5, 98.0, 100.0, 98.5, 90.1, 70.0, 45.5, 25.0])

# Fit Weibull distribution to the data
shape, loc, scale = weibull_min.fit(power_data, floc=0)  # floc=0 to force fit without shifting

# Generate Weibull distribution based on fitted parameters
x = np.linspace(0, np.max(power_data) * 1.2, 100)
pdf = weibull_min.pdf(x, shape, loc, scale)

# Plotting the histogram of power generation data
plt.figure(figsize=(8, 6))
plt.hist(power_data, bins=15, density=True, alpha=0.7, color='blue', edgecolor='black', label='Observed Data')

# Plot the fitted Weibull distribution
plt.plot(x, pdf, 'r-', lw=2, label=f'Fitted Weibull Distribution\nShape={shape:.2f}, Scale={scale:.2f}')

plt.title('Fitted Weibull Distribution to Power Generation Data')
plt.xlabel('Power Generation')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.show()

print(f"Fitted Weibull parameters: Shape = {shape:.2f}, Scale = {scale:.2f}")



import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

# Parameters for Beta distribution (shape parameters)
alpha = 2.0
beta_param = 5.0

# Generate random samples from the Beta distribution
num_samples = 1000
wind_generation = beta.rvs(alpha, beta_param, size=num_samples)

# Plotting the histogram of wind generation
plt.figure(figsize=(8, 6))
plt.hist(wind_generation, bins=30, density=True, alpha=0.7, color='blue', edgecolor='black')

# Plot the probability density function (PDF) of the Beta distribution
x = np.linspace(0, 1, 100)
pdf = beta.pdf(x, alpha, beta_param)
plt.plot(x, pdf, 'r-', lw=2, label='Beta PDF')

plt.title('Wind Generation Distribution (Beta)')
plt.xlabel('Wind Generation')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.show()



import numpy as np
import matplotlib.pyplot as plt

# Parameters for Beta distribution (shape parameters)
alpha = 2.0
beta_param = 5.0

# Generate random samples from the Beta distribution using numpy.random
num_samples = 1000
wind_generation = np.random.beta(alpha, beta_param, size=num_samples)

# Plotting the histogram of wind generation
plt.figure(figsize=(8, 6))
plt.hist(wind_generation, bins=30, density=True, alpha=0.7, color='blue', edgecolor='black')

# Plot the probability density function (PDF) of the Beta distribution
x = np.linspace(0, 1, 100)
pdf = beta.pdf(x, alpha, beta_param)
plt.plot(x, pdf, 'r-', lw=2, label='Beta PDF')

plt.title('Wind Generation Distribution (Beta)')
plt.xlabel('Wind Generation')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)
plt.show()



import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

# Example power generation data (replace this with your actual data)
power_data = np.array([0.2, 1.5, 5.0, 10.2, 20.0, 35.5, 50.1, 70.2, 90.5, 98.0, 100.0, 98.5, 90.1, 70.0, 45.5, 25.0])

# Normalizing the data to [0, 1] range
min_power = np.min(power_data)
max_power = np.max(power_data)
normalized_power_data = (power_data - min_power) / (max_power - min_power)

# Ensure the normalized data is strictly within (0, 1) by trimming edge values
normalized_power_data = np.clip(normalized_power_data, 1e-6, 1 - 1e-6)

# Fit Beta distribution to normalized data
alpha, beta_param, loc, scale = beta.fit(normalized_power_data, floc=0, fscale=1)

# Generate random samples from the Beta distribution using numpy.random
num_samples = 1000
beta_samples = np.random.beta(alpha, beta_param, size=num_samples)

# De-normalize the Beta samples back to the original scale
denormalized_samples = beta_samples * (max_power - min_power) + min_power

# Plotting the histogram of original and generated power data
plt.figure(figsize=(12, 6))

# Histogram of the original power data
plt.subplot(1, 2, 1)
plt.hist(power_data, bins=15, density=True, alpha=0.7, color='blue', edgecolor='black', label='Original Data')
plt.title('Original Power Generation Data')
plt.xlabel('Power Generation')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)

# Histogram of the generated power data
plt.subplot(1, 2, 2)
plt.hist(denormalized_samples, bins=30, density=True, alpha=0.7, color='green', edgecolor='black', label='Generated Data')

# Plot the PDF of the fitted Beta distribution (denormalized)
x = np.linspace(0, 1, 100)
pdf = beta.pdf(x, alpha, beta_param)
denormalized_x = x * (max_power - min_power) + min_power
plt.plot(denormalized_x, pdf * (1 / (max_power - min_power)), 'r-', lw=2, label='Fitted Beta PDF')

plt.title('Generated Power Generation Data')
plt.xlabel('Power Generation')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

print(f"Fitted Beta parameters: alpha = {alpha:.2f}, beta = {beta_param:.2f}")
