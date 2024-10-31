import pygame, random, spritesheet
pygame.init()

ss = spritesheet.Spritesheet(pygame.image.load("./Assets/Asteroids/asteroidSpritesheet4.png"))

class Object(pygame.sprite.Sprite):
    def __init__(self, asteroids, dim, score):
        super().__init__()
        randNum = random.randint(0, len(asteroids) - 1)
        while score < 1800 and randNum == len(asteroids) - 1:
            randNum = random.randint(0, len(asteroids) - 1)
        self.img = pygame.transform.scale_by(asteroids[randNum], random.uniform(0.8, 1.5)).convert_alpha()
        self.vel = [random.randint(-360, 360) * dim[0]/1920, random.randint(60, 270) * dim[0]/1080]
        self.size = self.img.get_width()
        self.dim = dim
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = pygame.Rect((random.randint(0, int(dim[0]) - self.size), -self.size), (self.size, self.size))
        self.type = "asteroid"

    def move(self, deltaTime):
        if self.rect.x < 0:
            self.rect.x = 0
            self.vel[0] *= -1

        elif self.rect.x > self.dim[0] - self.size:
            self.rect.x = self.dim[0] - self.size
            self.vel[0] *= -1

        self.rect.x += self.vel[0] * deltaTime * 2
        self.rect.y += self.vel[1] * deltaTime * 2

class Planet(pygame.sprite.Sprite):
    def __init__(self, dimensions):
        super().__init__()
        self.img = pygame.transform.scale(pygame.image.load("./Assets/Planet/planetHalf.png"), (dimensions[0], dimensions[0]/2)).convert_alpha()
        self.rect = self.img.get_rect()
        self.dimensions = dimensions
        self.rect.y = -dimensions[0]/2
        self.yOff = 0
        self.vel = dimensions[1]/25 * 1/20
        self.type = "planet"
        surface = pygame.Surface((self.img.get_width(), self.img.get_height()), pygame.SRCALPHA)
        surface.blit(self.img, (0, 0))
        self.mask = pygame.mask.from_surface(surface)
        
    def move(self, deltaTime):
        self.rect.y += self.vel

class AsteroidManager():
    def __init__(self, dim, mode):
        self.asteroidSprites = ss.getSprites(64, 1, dim[0]/512)[0]
        self.activeAsteroids = [Object(self.asteroidSprites, dim, 0)]
        self.displayInfo = dim
        self.score = 0
        self.count = 0
        self.next = 100
        self.new = True
        self.mode = mode
        self.planet = None

    def posUpdate(self, dt):
        if self.score >= self.next and self.new:
            self.count += 1
            self.next = 100 * 3**(len(self.activeAsteroids))
            self.new = False
            
        for i in range(len(self.activeAsteroids)):
            self.activeAsteroids[i].move(dt)

            if self.activeAsteroids[i].type == "asteroid" and self.activeAsteroids[i].rect.y > self.displayInfo[1]:
                self.new = True
                self.activeAsteroids.pop(i)
                self.count += 1
                self.score += 10
                break

        for i in range(self.count):
            if self.mode != 3 or self.score < 2500:
                self.activeAsteroids.append(Object(self.asteroidSprites, self.displayInfo, self.score))

        if self.score >= 2500 and self.mode == 3 and self.planet == None:
            self.planet = Planet(self.displayInfo)
            self.activeAsteroids.append(self.planet)

        self.count = 0

    def newAst(self):
        self.count += 1

    def blit(self, WIN):
        for i in self.activeAsteroids:
            WIN.blit(i.img, i.rect)
