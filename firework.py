import random

import pygame
import math


class Firework:
    def __init__(self, identifier, position, color, size):
        self.identifier = identifier
        self.position = position
        self.color = color
        self.size = size
        self.is_launched = False
        self.is_exploded = False
        self.particles = []

    def launch(self):
        self.is_launched = True

    def explode(self):
        if self.is_launched:
            self.is_exploded = True
            self.create_particles()

    def create_particles(self):
        for _ in range(100):
            angle = math.radians(random.uniform(0, 360))
            radius = random.uniform(1, 50)
            speed = random.uniform(1, 3)
            particle = Particle(self.position, self.color, angle, radius, speed)
            self.particles.append(particle)

    def update_particles(self):
        for particle in self.particles:
            particle.update()

    def draw(self, screen):
        if self.is_launched and not self.is_exploded:
            pygame.draw.circle(screen, self.color, self.position, 5)
        elif self.is_exploded:
            for particle in self.particles:
                particle.draw(screen)


class Particle:
    def __init__(self, position, color, angle, radius, speed):
        self.position = list(position)
        self.color = pygame.Color(color[0], color[1], color[2])  # Convert color to pygame.Color object
        self.angle = angle
        self.radius = radius
        self.speed = speed
        self.velocity = [self.speed * math.cos(self.angle), self.speed * math.sin(self.angle)]
        self.gravity = 0.05
        self.creation_time = pygame.time.get_ticks()
        self.fading_duration = 2500  # 3 seconds
        self.fading = False

    def update(self):
        self.velocity[1] += self.gravity
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Calculate the elapsed time since particle creation
        elapsed_time = pygame.time.get_ticks() - self.creation_time

        # Check if the elapsed time exceeds the fading duration
        if elapsed_time >= self.fading_duration:
            self.fading = True

        # Fade the color of the particle if fading is enabled
        if self.fading:
            fading_factor = max(0, 1 - (elapsed_time - self.fading_duration) / (self.fading_duration*5))
            self.color.r = min(int(self.color.r * fading_factor), 255)
            self.color.g = min(int(self.color.g * fading_factor), 255)
            self.color.b = min(int(self.color.b * fading_factor), 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), 2)



