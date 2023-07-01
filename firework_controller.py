import random
from firework import Firework

class FireworkController:
    def __init__(self):
        self.fireworks = []

    def add_firework(self, firework):
        self.fireworks.append(firework)

    def remove_firework(self, firework):
        self.fireworks.remove(firework)

    def initiate_firing_sequence(self):
        for firework in self.fireworks:
            firework.launch()


def create_random_firework(controller, screen_width, screen_height):
    identifier = len(controller.fireworks) + 1
    position = (random.randint(100, screen_width - 100), screen_height)
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    size = random.choice(["small", "medium", "large"])
    firework = Firework(identifier, position, color, size)
    controller.add_firework(firework)
