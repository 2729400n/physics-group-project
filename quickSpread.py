import numpy as np

def solve_laplace_equation(grid_size, condition_enforcer:'function'):
    """Solves the Laplace equation using a finite difference scheme.

    Args:
        grid_size: A tuple (x_size, y_size) specifying the grid dimensions.
        boundary_conditions: A NumPy array representing the boundary conditions.

    Returns:
        A NumPy array representing the electric potential at all grid points.
    """

    x_size, y_size = grid_size
    potential = np.zeros((x_size, y_size))
    potential = condition_enforcer(potential)

    #Iterate until convergence
    while True: 
        potential_new = np.copy(potential)
        max_diff = 0

        potential_new[1:-1, 1:-1] = 0.25 * (potential[:-2, 1:-1] + potential[2:, 1:-1] + potential[1:-1, :-2] + potential[1:-1, 2:])
        potential_new = condition_enforcer(potential_new)
        max_diff = np.max(np.abs(potential_new - potential))

        potential = potential_new 

        if max_diff < 1e-6:
            break

    return potential

# Example usage
grid_size = (50, 50)


def condition(state_grid:np.ndarray):
    state_grid[0,:] = 100 # Set Boundary Condtition
    return state_grid

potential = solve_laplace_equation(grid_size, condition_enforcer=condition)

import matplotlib.pyplot as plt
plt.imshow(potential, cmap='viridis')
plt.colorbar(label='Electric Potential')
plt.title('Electric Potential Distribution')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

import numpy as np
from scipy.ndimage import gaussian_filter

def create_pixelated_circle(size, radius, antialias_sigma=1):
    """Generates a pixelated circle with anti-aliasing.

    Args:
        size: A tuple (width, height) specifying the image dimensions.
        radius: The radius of the circle.
        antialias_sigma: The standard deviation for Gaussian blurring (anti-aliasing).

    Returns:
        A NumPy array representing the pixelated circle.
    """

    width, height = size
    center_x, center_y = width // 2, height // 2
    grid_x, grid_y = np.mgrid[:width, :height]
    circle_mask = (grid_x - center_x)**2 + (grid_y - center_y)**2 <= radius**2

    # Apply anti-aliasing using Gaussian blur
    blurred_circle = gaussian_filter(circle_mask.astype(float), sigma=antialias_sigma)

    # Threshold to create a binary image (0 or 1)
    pixelated_circle = np.where(blurred_circle > 0.5, 1, 0)

    return pixelated_circle

# Example usage
circle_size = (200, 200)
circle_radius = 50
pixelated_circle = create_pixelated_circle(circle_size, circle_radius, antialias_sigma=2)

plt.imshow(pixelated_circle, cmap='gray')
plt.title('Pixelated Circle with Anti-aliasing')
plt.show()
