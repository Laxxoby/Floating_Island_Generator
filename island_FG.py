import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from math import sqrt
import random
import csv
import svgwrite

"""
This program generates a 3D visualization of a floating island made up of 3D cubes and creates an .svg file 
that shows a 2D visualization with the top view, displaying the number of blocks that should go on the bottom part.
"""

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def main():
    generate_platform()


class Cube:
    """
    Represents a cubic object in a three-dimensional system.

    Args:
    - origin (list): A list representing the [x, y, z] coordinates of the cube's origin.

    Attributes:
    - origin (list): [x, y, z] coordinates of the cube's origin.
    - vertices (numpy.ndarray): Matrix containing the coordinates of the cube's vertices.
    - faces (list): List containing the faces of the cube, defined by their vertices.
    """
    def __init__(self, origin): #example [0.5, 0.5, 0.5]
        x, y, z = origin[0], origin[1], origin[2]
        self.origin = origin
        self.vertices = np.array([
            [x - 0.5, y - 0.5, z - 0.5], [x + 0.5, y - 0.5, z - 0.5], [x + 0.5, y + 0.5, z - 0.5], [x - 0.5, y + 0.5, z - 0.5],  # Bottom face
            [x - 0.5, y - 0.5, z + 0.5], [x + 0.5, y - 0.5, z + 0.5], [x + 0.5, y + 0.5, z + 0.5], [x - 0.5, y + 0.5, z + 0.5]
        ])
        self.faces = [
            [self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]],  # Bottom face
            [self.vertices[4], self.vertices[5], self.vertices[6], self.vertices[7]],  # Top face
            [self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]],  # Side face
            [self.vertices[2], self.vertices[3], self.vertices[7], self.vertices[6]],  # Side face
            [self.vertices[1], self.vertices[2], self.vertices[6], self.vertices[5]],  # Back face
            [self.vertices[0], self.vertices[3], self.vertices[7], self.vertices[4]]   # Front face
        ]


def generate_platform():

    """
    Generates a three-dimensional platform formed by a set of cubes within a circle.

    Parameters:
    radius -- Radius of the circle defining the platform's shape.
    height -- Height of the platform.

    The function creates a three-dimensional platform within a circle with the given radius.
    Cubes are generated at positions within the circle and stacked based on the height,
    creating a visually representative structure of a platform.
    """
    
    # Function to validate input data
    radius, height, island_mode = validate_data()
    
    global ax
    center_x, center_y = radius + 1, radius + 1  # Calculate the image center
    height_array = np.zeros(((radius * 2) + 3, (radius * 2) + 3))
    
    for i in range((radius * 2) + 1):
        for j in range((radius * 2) + 1):
            distance = (i - center_x)**2 + (j - center_y)**2  # Calculate distance to center
            
            # If the distance is less than or equal to the squared radius, it's inside the circle
            if distance <= radius**2 - 1:
                box1 = Cube([i + 0.5, j + 0.5, height + 0.5])
                cube = Poly3DCollection(box1.faces, alpha=0.25, facecolors='green')
                ax.add_collection3d(cube)
                island_height = IslandHeight(distance, radius, height, i, j, island_mode)    
                height_array[i, j] = island_height     
                
    # create svg with heights
    create_square_svg(height_array, radius)
    
    # create csv with heights
    create_square_csv(height_array)
                
    # Set axis limits
    ax.set_xlim([0, (radius * 2) + 1])
    ax.set_ylim([0, (radius * 2) + 1])
    ax.set_zlim([0, height + 3])

    # Label axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Show the plot
    plt.show()

def IslandHeight(distance, radius, height, i, j, islandMode):
    """
    Calculates the height of each cube based on its distance from the center of the island and generates a 3D graphical representation.

    Parameters:
    distance -- Distance to the center of the island.
    radius -- Radius of the circle defining the island.
    height -- Maximum height the island can have.
    i -- x-coordinate of the cube.
    j -- y-coordinate of the cube.
    islandMode -- Island mode.

    Returns:
    Cubes_height -- Height of the generated cube.

    The function calculates the height of the cube depending on the provided distance and generates a set of cubes in a 3D graphical representation.
    Additionally, it adds text on top of some cubes showing the quantity of cubes at that position.
    """
    global ax
    percentage = ((abs(sqrt(distance) - radius)) / radius) * 100

    if percentage <= 100 and percentage > 80:
        Cubes_height = random.randint(1 if islandMode == "random" else int(height * 0.8), height)
    elif percentage <= 80 and percentage > 60:
        Cubes_height = random.randint(1 if islandMode == "random" else int(height * 0.6), int(height * 0.8))
    elif percentage <= 60 and percentage > 40:
        Cubes_height = random.randint(1 if islandMode == "random" else int(height * 0.4), int(height * 0.6))
    elif percentage <= 40 and percentage > 20:
        Cubes_height = random.randint(1 if islandMode == "random" else int(height * 0.2), int(height * 0.4))
    elif percentage <= 20 and percentage > 0:
        Cubes_height = random.randint(1, int(height * 0.2))
        # ax.text(i + 0.5, j + 0.5, height + 1.5, str(Cubes_height), color='red', fontsize=10, ha='center')

    for z in range(Cubes_height + 1):
        box = Cube([i + 0.5, j + 0.5, (height - 0.5) - z])
        cube = Poly3DCollection(box.faces, alpha=0.25, facecolors='cyan' if z % 2 == 0 else 'blue')
        ax.add_collection3d(cube)

    return Cubes_height

def create_square_svg(HeightArr, radius=1):
    rows, columns = HeightArr.shape
    side = 300 / radius 
    space_between_squares = side * 0.1
    dwg = svgwrite.Drawing('2dPlane.svg', profile='full')

    for i in range(rows):
        for j in range(columns):
            x = j * (side + space_between_squares)  # Add horizontal space between squares
            y = i * (side + space_between_squares)  # Add vertical space between squares
            number = int(HeightArr[i, j])
            dwg.add(dwg.rect(insert=(x, y), size=(side, side), fill='#1C2833' if number == 0 else '#138D75'))
            
            dwg.add(dwg.text((str(number) if number > 0 else ""), insert=(x + side / 2, y + side / 2), fill='#F4F6F7', font_size=0.3 * side, text_anchor='middle', alignment_baseline='middle'))

    dwg.save()

def create_square_csv(heights):
    file_name = 'heights.csv'
    
    # Write the matrix into the CSV file
    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in heights:
            csv_writer.writerow(row)

def validate_data():
    print("Welcome to the floating islands generator for Minecraft")
    radius = validate_number("Enter the radius of the upper circular platform: ")
    height = validate_number("Enter the maximum height the floating island can have: ", 5)
    mode = validate_mode()
    return radius, height, mode

def validate_number(message, min_value=1):
    while True:
        try:
            value = int(input(message))
            if value < min_value:
                print("Please enter a number greater than or equal to", min_value)
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")

def validate_mode():
    while True:
        mode = input("Enter the mode in which the Floating Island will be created (random or semiUniform): ").lower()
        if mode in ["random", "semiuniform"]:
            return mode
        print("Please enter 'random' or 'semiuniform'.")

if __name__ == '__main__':
    main()
