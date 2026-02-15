import pygame
import os

class Visuals:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 480)) # Adjust for 5-inch screen
        self.faces = {
            "idle": pygame.image.load("assets/idle.png"),
            "thinking": pygame.image.load("assets/thinking.png"),
            "speaking": pygame.image.load("assets/speaking.png")
        }

    def show(self, state):
        self.screen.fill((0, 0, 0)) # Clear screen
        img = self.faces.get(state, self.faces["idle"])
        self.screen.blit(img, (0, 0))
        pygame.display.flip()