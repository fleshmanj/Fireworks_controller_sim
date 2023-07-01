import pygame
import random
import math
from firework import Firework, Particle
from firework_controller import FireworkController

# Pygame initialization
pygame.init()
clock = pygame.time.Clock()
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Fireworks Display")

# Colors
BLACK = (0, 0, 0)

# Firework parameters
launch_interval = 0.3  # Time interval between launching each firework (in seconds)
explosion_duration = 5  # Duration of the firework explosion (in seconds)


# Firework Controller
controller = FireworkController()


# Function to create a random firework
def create_random_firework():
    identifier = len(controller.fireworks) + 1
    position = (random.randint(200, screen_width - 200), random.randint(200, math.floor(screen_height/2) - 200))
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    radius = random.randint(3, 5)  # Random radius for the firework
    firework = Firework(identifier, position, color, radius)

    # Set initial velocity for firework particles
    for particle in firework.particles:
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 5)
        particle.velocity = [speed * math.cos(angle), -speed * math.sin(angle)]

    controller.add_firework(firework)
    print(f"Firework {firework.identifier} created at position {firework.position}")


# Game loop
running = True
while running:
    number_of_fireworks = random.randrange(1, 4)  # Number of fireworks to launch at the start of the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    if len(controller.fireworks) == 0:
        for i in range(0, number_of_fireworks):
            create_random_firework()

    # Update and draw fireworks
    for firework in controller.fireworks:
        if not firework.is_launched:
            firework.launch()
            print(f"Firework {firework.identifier} launched!")
        elif firework.is_launched and not firework.is_exploded:
            firework.explode()
            explosion_start_time = pygame.time.get_ticks()
            print(f"Firework {firework.identifier} exploded!")

        # Calculate explosion progress
        if firework.is_exploded:
            explosion_elapsed_time = (pygame.time.get_ticks() - explosion_start_time) / 1000
            if explosion_elapsed_time >= explosion_duration:
                controller.remove_firework(firework)
                print(f"Firework {firework.identifier} removed.")
            else:
                firework.update_particles()

        # Draw firework and particles
        firework.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
