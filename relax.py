# A alogithm for relaxing points to equalize the distance between them

import numpy as np
import matplotlib.pyplot as plt


# Size of sphere for points to lie on
RADIUS = 1
NUM_POINTS = 30
NEAREST_NEIGHBORS = 5 # Number of nearest neighbors to consider when relaxing points

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

def main():      
    points = sample_sphere(NUM_POINTS)
    next_points = []
    avg_difference = 1
    
    while avg_difference > 0.01:
        avg_difference = 0
        print("Points: ", points)
        for point in points:
            # Determine the distance to the points to every other point
            distances = {}
            for other_point in points:
                if other_point == point:
                    continue
                distance = np.linalg.norm(np.array(point) - np.array(other_point))
                distances[other_point] = distance
                # Sort the distances
                distances = {key: value for key, value in sorted(distances.items(), key=lambda item: item[1])}
            # Calculate the average of the 3 closest points
            closest_points = list(distances.keys())[:NEAREST_NEIGHBORS]
            avg_point = np.mean(closest_points, axis=0)
            next_points.append((avg_point[0], avg_point[1], avg_point[2]))
            avg_difference += np.linalg.norm(np.array(point) - np.array(avg_point))
            
        
        avg_difference /= len(points)
        print("Avg Difference: ", avg_difference)
        
        # Update the points
        points = next_points
        next_points = []
    
    
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_box_aspect([1,1,1])
    ax.set_proj_type('ortho')
    ax.set_axis_off()
    ax.set_title("Relaxation of Points on Sphere")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.scatter(*zip(*points), color='black')
    plt.show()
    

    print()

if __name__ == "__main__":
    main()
