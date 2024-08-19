# A alogithm for relaxing points to equalize the distance between them

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Size of sphere for points to lie on
RADIUS = 1              # Radius of the sphere
NUM_POINTS = 10         # Number of points to generate on the sphere
DELAY = 1               # Delay between iterations in milliseconds

FORCE = 1.0             # The force of the repelling force between points
LEARNING_RATE = 0.01    # The learning rate for the relaxation algorithm

def sample_sphere(num_points: int) -> list:
    """
    Generates a list of points on a sphere of radius 1.

    Args:
        num_points (int): The number of points to generate.
    """
    points = []
    for _ in range(num_points):
        # Generate a random point on the sphere using spherical coordinates
        theta = np.random.uniform(0, 2*np.pi)
        phi = np.random.uniform(0, np.pi)
        x = RADIUS * np.sin(phi) *np.cos(theta)
        y = RADIUS * np.sin(phi) *np.sin(theta)
        z = RADIUS * np.cos(phi)
        points.append((x, y, z))
    return points


def relax_points(points: list, ax) -> None:
    """
    Relaxes the points on the sphere.

    Args:
        points (list): The points to relax.
    """
    difference = 1
    while difference > 0.001:
        difference = 0
        
        ax.scatter(*zip(*points))
        plt.pause(1)
        plt.draw()
                
        # Calculate the total force vectors between all points
        forces = np.zeros_like(points)
        for point_index in range(len(points)):
            for comparison_index in range(len(points)):
                if point_index != comparison_index:
                    point_vector = np.array(points[point_index]) - np.array(points[comparison_index])
                    point_distance = np.linalg.norm(point_vector)
                    if point_distance == 0:
                        continue
                    point_interaction_force = FORCE * point_vector / point_distance**3
                    
                    # Add force to the point
                    forces[point_index] += point_interaction_force
        
        # Update the points with the forces
        old_points = np.copy(points)
        for point_index in range(len(points)):
            points[point_index] += LEARNING_RATE * forces[point_index]
            # Normalise to keep the points on the sphere
            points[point_index] /= np.linalg.norm(points[point_index])/RADIUS
        
        difference = np.linalg.norm(points - old_points)
        

def main():      
    points = sample_sphere(NUM_POINTS)
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_box_aspect([1,1,1])
    ax.set_proj_type('ortho')
    ax.set_axis_off()
    ax.set_title("Relaxation of Points on Sphere")
    ax.set_xlim(-RADIUS, RADIUS)
    ax.set_ylim(-RADIUS, RADIUS)
    ax.set_zlim(-RADIUS, RADIUS)
    
    ani = FuncAnimation(fig, relax_points(points, ax), interval=DELAY)
    plt.show()


if __name__ == "__main__":
    main()
