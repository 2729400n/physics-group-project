import unittest
import numpy as np
import matplotlib.pyplot as plt
from Numerical_Methods.utils.custom_cmap_maker import makeCustomCmap, loadCMap
from Numerical_Methods.legacy.utils import laplace_ode_solver, makeGeometry2, BoxinBox, doNothing
from Numerical_Methods.legacy.quickSpread import solve_laplace_equation, create_pixelated_circle

class TestCustomCmapMaker(unittest.TestCase):

    def test_makeCustomCmap(self):
        cmap = makeCustomCmap()
        self.assertEqual(len(cmap), 256 * 5 -2)  # Check the number of colors generated
        self.assertTrue(all(c.startswith('#') and len(c) == 7 for c in cmap))  # Check color format

    def test_storeCMap(self):
         #Indirect test. Check if file exists. Ideally mock file operations in future
        try:
            cmap = loadCMap()
            self.assertTrue(len(cmap)>0)
        except Exception as e:
            self.fail(f"Failed to load colormap file: {e}")

class TestUtils(unittest.TestCase):

    def test_laplace_ode_solver_simple(self):
        # Test with a simple case (e.g., constant boundary conditions)
        size = (10, 10)
        fixed_conditions = lambda x: np.ones_like(x)  #Constant boundary
        start_shape = lambda x: np.zeros_like(x)

        ys, xs, potential = laplace_ode_solver(size, fixed_conditions, start_shape, (1,1),overlaySaver=False)
        fig=plt.figure()
        plt.imshow(potential)
        plt.suptitle('LP Solver!')
        plt.colorbar()
        plt.savefig('test_legacy_ode_solver_simple.png')
        
        self.assertTrue(np.allclose(potential, 1)) # expect potential to converge to boundary value


    def test_laplace_ode_solver_convergence(self):
        size = (20, 20)
        # Test to ensure the solver converges (doesn't oscillate or diverge).
        # Mock boundary conditions and start shape
        fixed_conditions = lambda x: x
        fixed_conditions = makeGeometry2()
        ys, xs, potential = laplace_ode_solver(size, fixed_conditions, fixed_conditions,(1,1))
        self.assertTrue(np.all(np.isfinite(potential)))  # Check for NaN or Inf values


    def test_makeGeometry2(self):
        grid = np.zeros((10, 10))
        end_to_end_line = makeGeometry2(val=1.0, r=1.0, cx=0.5, cy=0.5)
        result_grid = end_to_end_line(grid.copy())
        self.assertTrue(np.all(result_grid[:, (0, -1)] == 1.0)) # Check edges
        # Add more checks based on the expected shape

    def test_BoxinBox(self):
        grid = np.zeros((10, 10))
        result_grid = BoxinBox(grid.copy(),r=0.5)  # Use a radius value
        self.assertTrue(np.all(result_grid[:, (0, -1)] == 1.0)) # Check edges
        # Check if the inner circle area values are as expected.

class TestQuickSpread(unittest.TestCase):

    def test_solve_laplace_equation(self):
        grid_size = (20, 20)
        def condition(state_grid: np.ndarray):
            state_grid[(0, -1), :] = 100
            return state_grid
        potential = solve_laplace_equation(grid_size, condition_enforcer=condition)
        self.assertTrue(np.all(np.isfinite(potential))) # Check for NaN/Inf

    def test_create_pixelated_circle(self):
        circle_size = (50, 50)
        radius = 20
        circle = create_pixelated_circle(circle_size, radius)
        self.assertEqual(circle.shape, circle_size)  # Check dimensions
        # Add checks to verify circle properties like radius and center

if __name__ == '__main__':
    unittest.main()
