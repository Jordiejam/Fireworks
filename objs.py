import pygame
import random
from copy import copy

class Firework():
    
    gravity = 0.1
    max_trail = 20
    
    def __init__(self, screen:pygame.Surface,):
        self.screen = screen
        
        max_velocity = self.screen.get_height()/60
        self.vel = random.random()*(max_velocity-6)+6
        self.size = random.randint(2, 5)
        self.pos = pygame.Vector2((random.randint(10, self.screen.get_width()-10), self.screen.get_height()))
        self.colour = (random.randint(5, 255), random.randint(5, 255), random.randint(5, 255))
        self.tilt = random.random()*random.randint(-1,1)
        self.particles = []
        self.trail = []

        self.firework_explosion_sound = pygame.mixer.Sound("assets\\single-firework-79814.wav")

        self.exploded = False

    def update(self):
        if not self.exploded:
            if len(self.trail) > self.max_trail:
                self.trail.pop(0)
            self.trail.append(self.pos.copy())
            self.pos.y -= self.vel
            self.pos.x += self.tilt
            self.vel -= self.gravity
            #self.tilt *= 0.99
        else:
            for i in range(len(self.particles)-1, -1, -1):
                self.particles[i].update()
                if self.particles[i].complete:
                    self.particles.pop(i)

    def explode(self):
        if self.vel <= 3:
            if not self.exploded:
                if random.random() < 0.1:
                    self.exploded = True
                    self.firework_explosion_sound.play()
                    self.particles = [Particle(self) for _ in range(20)]
        
        if self.exploded:
            return True

    def show(self):
        if not self.exploded:
            for i, pos in enumerate(self.trail):
                fade_amount = (i + 1) / (self.max_trail + 1)
                faded_colour = tuple(int(c * fade_amount) for c in self.colour)
                pygame.draw.circle(self.screen, faded_colour, pos, self.size)
            pygame.draw.circle(self.screen, self.colour, self.pos, self.size)
        else:
            for p in self.particles:
                p.show()

class Particle():

    max_trail = 7

    def __init__(self, firework:Firework) -> None:
        self.firework = firework
        self.size = self.firework.size*0.8
        self.og_pos = firework.pos
        self.pos = self.og_pos.copy()
        self.colour = copy(self.firework.colour)

        self.alpha = 255

        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(2, 4)

        self.initial_lifespan = random.randint(25, 50)
        self.lifespan = int(self.initial_lifespan)
        self.trail = []

        self.complete = False

    def update(self):
        if self.lifespan > 0:
            self.lifespan -= 1
            self.size = max(self.firework.size * 0.8 * (self.lifespan / self.initial_lifespan), 1)

            if len(self.trail) > self.max_trail:
                self.trail.pop(0)
            self.trail.append((self.pos.copy(), self.alpha))
            
            fade_ratio = self.lifespan / 100
            self.alpha = int(255 * fade_ratio)

            self.pos += self.velocity
            self.velocity.y += self.firework.gravity*0.3
        else:
            self.complete = True
            self.size = 0

    def show(self):
        
        for i, tup in enumerate(self.trail):
                # Calculate fading colour based on trail position
                fade_amount = (i + 5) / (self.max_trail + 5)  # Adjust fade_amount so the final particle isn't black
                faded_colour = tuple(int(c * fade_amount) for c in self.colour)
                pygame.draw.circle(self.firework.screen, faded_colour, tup[0], self.size)

        if self.size > 0:
            # Use a surface to apply alpha for fading out
            surface = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(surface, self.colour + (self.alpha,), (int(self.size), int(self.size)), int(self.size))
            self.firework.screen.blit(surface, (int(self.pos.x - self.size), int(self.pos.y - self.size)))