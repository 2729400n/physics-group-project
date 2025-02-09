import numpy as np
import matplotlib.pyplot as plt

# Parameters
r1 = 10  # Inner radius for the potential region
r2 = r1*2
d = 55  # Grid limit for x and y
num_points = 1000  # Number of points for the grid resolution
 
# Generate a grid of x and y values for the vector field
x_vals = np.linspace(-d, d, 40)
y_vals = np.linspace(-100, 100, 40)
 
# Create meshgrid for plotting
x, y = np.meshgrid(x_vals, y_vals)
 
# Calculate the radial distance from the origin
r = np.sqrt(x**2 + y**2)
 
# Only keep values where r >= r1 (mask the region inside r1)
mask = r1 <= r <= r2
 
# Initialize the components of the vector field (u and v)
u = np.zeros_like(x)
v = np.zeros_like(y)
 
# Compute the electric field components only for points where r >= r1
V = 1  # Potential scaling constant (set appropriately for your problem)
for i in range(len(x_vals)):
    for j in range(len(y_vals)):
        if mask[j, i]:  # Only process points where r >= r1
            r_ij = r[j, i]
            theta = np.arctan2(y[j, i], x[j, i])  # Angle for polar coordinates
 
            # Radial component (dV/dr)
            dV_dr = (V/d)*(np.cos(theta)*(r1**2)/r_ij**2 + np.cos(theta))
 
            # Angular component (dV/dtheta)
            dV_dtheta = (V/d)*(np.sin(theta)*(r1**2)/r_ij**2 - np.sin(theta))
 
            # Convert the polar electric field components to Cartesian components
            u[j, i] = -dV_dr * np.cos(theta) + dV_dtheta * np.sin(theta)
            v[j, i] = -dV_dr * np.sin(theta) + dV_dtheta * np.cos(theta)
 
 
# Compute the potential (just an example, adjust formula as necessary)
 
pot = (np.sqrt(x**2+y**2) - np.sqrt(x**2+y**2) * r1**2) * (-V/d * np.cos(np.arctan2(y, x)))
 
 
plt.figure(figsize=(12, 12))
 
# Plot the potential using pcolormesh
plt.pcolormesh(x, y, pot, shading='auto', cmap='PiYG')
plt.colorbar(label="Potential")
 
# Plot the vector field using quiver
plt.quiver(x, y, u, v, angles='xy', scale_units='xy', scale=.005, color='black')
 
# Add a circle at r1 (boundary of the region where r >= r1)
theta_circle = np.linspace(0, 2 * np.pi, 1000)
x_circle1 = r1 * np.cos(theta_circle)
y_circle1 = r1 * np.sin(theta_circle)
 
# Plot the circle at r1
plt.plot(x_circle1, y_circle1, color='black', linewidth=2)
 
# Set axis limits
plt.xlim(-d, d)
plt.ylim(-100, 100)
 
# Make the aspect ratio equal (circular plot)
plt.gca().set_aspect('equal', adjustable='box')
 
# Title and labels
plt.title("Vector Field of Electric Field (r >= r1)")
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
 
# Add grid for better visualization
plt.grid(True)
 
# Show the plot
plt.show()