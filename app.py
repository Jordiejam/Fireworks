import pygame
import sys
import random
from objs import *

# Initialize Pygame
pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Bonfire Night")
clock = pygame.time.Clock()

fireworks:list[Firework] = []

font = pygame.font.SysFont("Arial", 12)

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
    
    framerate = str(int(clock.get_fps()))
    text = font.render(framerate, True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
