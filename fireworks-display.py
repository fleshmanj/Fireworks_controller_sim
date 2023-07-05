import pygame
import random
import math
import PySimpleGUI as sg
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

# Initialize PySimpleGUI
sg.theme("DefaultNoMoreNagging")

# Define the layout of the UI
layout = [
    [sg.Text("Firework Configuration")],
    [sg.Text("Position (x, y):"), sg.Input(key="-POSITION-")],
    [sg.Text("Color (R, G, B):"), sg.Input(key="-COLOR-")],
    [sg.Text("Radius:"), sg.Input(key="-RADIUS-")],
    [sg.Button("Add Firework", key="-ADD-")],
    [sg.Button("Start Sequence", key="-START-")]
]

# Create the window
window = sg.Window("Fireworks Display", layout)

# List to store the queued fireworks configurations
fireworks_queue = []

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Create random fireworks at specified interval
    if pygame.time.get_ticks() % int(launch_interval * 1000) == 0:
        if fireworks_queue:
            config = fireworks_queue.pop(0)
            firework = Firework(len(controller.fireworks) + 1, config["position"], config["color"], config["radius"])
            controller.add_firework(firework)
            print(f"Firework {firework.identifier} created at position {firework.position}")

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

    # Update the Pygame display
    pygame.display.flip()
    clock.tick(60)

    # Process the UI events
    event, values = window.read(timeout=0)
    if event == "-ADD-":
        try:
            position = tuple(map(int, values["-POSITION-"].split(",")))
            color = tuple(map(int, values["-COLOR-"].split(",")))
            radius = int(values["-RADIUS-"])
            fireworks_queue.append({"position": position, "color": color, "radius": radius})
            print(f"Firework added to queue: {position}, {color}, {radius}")
        except ValueError:
            print("Invalid configuration. Please enter valid values.")
    elif event == "-START-":
        if fireworks_queue:
            print("Fireworks sequence started.")
        else:
            print("No fireworks in the queue.")

    if event == sg.WINDOW_CLOSED:
        break

# Close the Pygame display and the UI window
pygame.quit()
window.close()