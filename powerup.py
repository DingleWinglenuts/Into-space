import pygame, random

# This file contains an object that manages all active powerups and also another object for individual powerups. The process behind how it works is based off of the asteroid manager and asteroid objects in asteroids.py

class Powerup(pygame.sprite.Sprite): # Individual powerups
    def __init__(self, type, dim): # This init function is heavily based on the init function for the "Object" object in the asteroids.py file
        super().__init__() # Inherits properties from the pygame sprite class, which can be used to create masks, which have better collision detection than otherwise available
        self.img = pygame.transform.scale(pygame.image.load("./Assets/Powerup/powerup.png"), (dim[1]//8, dim[1]//8)).convert_alpha()
        self.vel = [random.randint(-60, 60) * dim[0]/1920, random.randint(60, 100) * dim[0]/1080] # Setting the speed in each direction (and thereby angle of movement) of powerups
        self.size = self.img.get_width()
        self.dim = dim # Stores the window size
        self.mask = pygame.mask.from_surface(self.img) # Creates a mask based on the powerup image
        self.rect = pygame.Rect((random.randint(0, int(dim[0]) - self.size), -self.size), (self.size, self.size)) # Stores all information about position and scale of the object
        self.type = type # Stores the type of powerup (health refill, shield, etc.)

    # Moves the powerup a certain distance based on time passed since the last frame (for consistency across devices)

    def move(self, deltaTime):
        # "Bouncing" powerups to keep them on the screen if they reach either edge of the screen
        # This works by inverting the + or - sign in front of the x velocity if the edge of the screen is reached

        if self.rect.x < 0: 
            self.rect.x = 0
            self.vel[0] *= -1

        elif self.rect.x > self.dim[0] - self.size:
            self.rect.x = self.dim[0] - self.size
            self.vel[0] *= -1

        # Moving the powerup

        self.rect.x += self.vel[0] * deltaTime * 2
        self.rect.y += self.vel[1] * deltaTime * 2

class Manager(): # Manager for all active powerups
    def __init__(self, dim, mode):
        self.mode = mode # Stores the selected gamemode
        self.dim = dim # Stores the window dimensions

        # Declares what powerups can be created (removes health powerups if the mode is one life)

        self.types = ["health", "shield", "speed boost", "score", "shrink"]
        if self.mode == 2:
            self.types.pop(0)

        self.powerups = [] # List storing active powerups

        # The next 2 variables are used for the chance of powerups spawning at any given time
        # The chance of a powerup spawning at any given time is 1/(81-x) * (1 - 1/(81-(x-1))) * (1 - 1/(81-(x-2))) (and so on until x is 0), where x is the number of seconds passed since the last powerup spawns (or since the start of the game if none have spawned before)
        # This will mean that there is a guaranteed chance of a powerup spawning after 80 seconds since the last, but there is a probability of a powerup spawning earlier than this 80 second mark

        self.time = 0 # Used to reattempt the probability every second
        self.upperBound = 80 # Used as a maximum boundary for the calculation (will decrease by 1 every second, hence the x-n part in the calculation)

    def spawn(self, dt):
        if self.time < 1: # Cancels the function if the time passed is less than 1
            self.time += dt # Accumulates the time passed
            return
        
        self.time -= 1 # Resets the time passed for the next time

        if random.randint(0, self.upperBound) == 0: # Spawns a powerup if the random generation produces a 0
            self.powerups.append(Powerup(self.types[random.randint(0, len(self.types) - 1)], self.dim))
            self.upperBound = 80 # Resets the probability of a powerup spawning to 1/80
        else: # Increases the chances of a powerup spawning if one hasnt spawned in the last attempt
            self.upperBound -= 1

    def move(self, dt):
        self.spawn(dt) # Attempts spawning a new powerup

        for i in range(len(self.powerups)):
            if i >= len(self.powerups): # Contingency to prevent a "list index out of range" error for if a powerup despawns during the loop
                break

            self.powerups[i].move(dt)
            if self.powerups[i].rect.y > self.dim[1]: # Removes the powerup if it goes out of sight
                self.powerups.pop(i)

    def blit(self, WIN): # Displays all active powerups
        for i in self.powerups:
            WIN.blit(i.img, i.rect)
