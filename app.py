import pygame
import sys
import random
from objs import *

# Initialize Pygame
pygame.init()

# Constants for screen dimensions
WIDTH = 800
HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Bonfire Night")
clock = pygame.time.Clock()

fireworks:list[Firework] = []

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((0, 0, 0))

    # Game logic
    if random.random() < 0.04:
        fireworks.append(Firework(screen))

    for i in range(len(fireworks)-1, -1, -1):
        fireworks[i].update()
        fireworks[i].show()
        if fireworks[i].explode():
            if not fireworks[i].particles:
                fireworks.remove(fireworks[i])

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
