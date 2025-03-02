import math
import random
import sys
import os

import neat  # NEAT (NeuroEvolution of Augmenting Topologies) for neural network evolution
import pygame  # For visualization and game mechanics

# Screen dimensions and game constants
WIDTH = 1920  # Screen width
HEIGHT = 1080  # Screen height
CAR_SIZE_X = 60  # Car width in pixels
CAR_SIZE_Y = 60  # Car height in pixels
BORDER_COLOR = (255, 255, 255, 255)  # Color that represents track boundaries

current_generation = 0  # Tracks the current generation of cars

class Car:
    """
    Represents a self-driving car in the simulation.
    Each car has:
    - Position and movement capabilities
    - Sensors (radars) to detect track boundaries
    - Neural network for decision making
    - Fitness tracking for evolution
    """
    def __init__(self):
        # Initialize car sprite and its properties
        self.sprite = pygame.image.load('car.png').convert()  # Load and optimize car image
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite 

        # Initial position and movement properties
        self.position = [830, 920]  # Starting position on the track
        self.angle = 0  # Current angle of rotation
        self.speed = 0  # Current speed
        self.speed_set = False  # Flag to set initial speed

        # Calculate center point of the car
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]

        # Initialize sensor arrays
        self.radars = []  # Stores radar data (distance to boundaries)
        self.drawing_radars = []  # Stores radar visualization data

        # State tracking
        self.alive = True  # Whether the car is still in the race
        self.distance = 0  # Total distance traveled
        self.time = 0  # Time spent in the race

    def draw(self, screen):
        """Draw the car and its sensors on the screen"""
        screen.blit(self.rotated_sprite, self.position)
        self.draw_radar(screen)  # Draw sensor visualization

    def draw_radar(self, screen):
        """Visualize the car's sensors on the screen"""
        for radar in self.radars:
            position = radar[0]
            # Draw sensor lines and detection points
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_collision(self, game_map):
        """Check if the car has collided with track boundaries"""
        self.alive = True
        for point in self.corners:
            # Check each corner of the car for collision with track boundaries
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    def check_radar(self, degree, game_map):
        """Simulate a radar sensor at a specific angle to detect track boundaries"""
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Extend radar until it hits a boundary or reaches max length
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calculate and store distance to boundary
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])
    
    def update(self, game_map):
        """Update car's position, check collisions, and update sensors"""
        # Set initial speed if not already set
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        # Update car's position and rotation
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        # Update distance and time metrics
        self.distance += self.speed
        self.time += 1
        
        # Update Y position with boundary checks
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

        # Update center point
        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        # Calculate car's corner points for collision detection
        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check for collisions and update sensors
        self.check_collision(game_map)
        self.radars.clear()

        # Update all radar sensors
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def get_data(self):
        """Get normalized sensor data for neural network input"""
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)  # Normalize distances
        return return_values

    def is_alive(self):
        """Check if car is still in the race"""
        return self.alive

    def get_reward(self):
        """Calculate fitness reward based on distance traveled"""
        return self.distance / (CAR_SIZE_X / 2)

    def rotate_center(self, image, angle):
        """Rotate the car sprite while maintaining its center point"""
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image


def run_simulation(genomes, config):
    """
    Main simulation function that runs the NEAT algorithm and visualizes the cars
    Args:
        genomes: List of genomes for the current generation
        config: NEAT configuration parameters
    """
    # Initialize neural networks and cars
    nets = []
    cars = []

    # Set up Pygame display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    # Create neural networks for each genome
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())

    # Initialize game elements
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load('map4.png').convert()

    global current_generation
    current_generation += 1

    counter = 0  # Time counter for simulation

    while True:
        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # Process each car's neural network output
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10  # Turn left
            elif choice == 1:
                car.angle -= 10  # Turn right
            elif choice == 2:
                if(car.speed - 2 >= 12):
                    car.speed -= 2  # Slow down
            else:
                car.speed += 2  # Speed up
        
        # Update cars and track fitness
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()

        # End generation if all cars are dead
        if still_alive == 0:
            break

        # End generation after time limit
        counter += 1
        if counter == 30 * 40:  # ~20 seconds
            break

        # Draw game elements
        screen.blit(game_map, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)
        
        # Display generation and alive count
        text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    # Load NEAT configuration
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create and configure the population
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run the simulation for 1000 generations
    population.run(run_simulation, 1000)
