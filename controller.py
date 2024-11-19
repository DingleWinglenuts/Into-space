import pygame, pygame._sdl2.controller; from math import sin, cos, atan, pi
pygame._sdl2.controller.init()

class Controller:
    def __init__(self, speed):
        self.controller = pygame._sdl2.controller.Controller(0)
        self.joystickX = 0
        self.joystickY = 0
        self.moveSpeed = 0
        self.speedX = 0
        self.speedY = 0
        self.speed = speed
        self.joystickDeadzone = 0.2
        self.triggerDeadzone = 0.2
        self.rightTrigger = False
        self.firstPress = False
        self.boosting = False

        self.lastRumble = 0
        self.powerupRumble = False
        self.powerupRumbleCount = 0

    def update(self):
        self.joystickX = self.controller.get_axis(pygame.CONTROLLER_AXIS_LEFTX)/32768
        self.joystickY = -self.controller.get_axis(pygame.CONTROLLER_AXIS_LEFTY)/32768
        self.moved = False
        
        if self.controller.get_axis(pygame.CONTROLLER_AXIS_TRIGGERRIGHT)/32768 - self.triggerDeadzone > 0:
            if not self.rightTrigger:
                self.firstPress = True
            else:
                self.firstPress = False
            self.rightTrigger = True
        else:
            if self.rightTrigger:
                self.released = True
            else:
                self.released = False
            self.rightTrigger = False
        
        moveSpeed = ((self.joystickX * self.speed) ** 2 + (self.joystickY * self.speed) ** 2) ** 0.5

        if moveSpeed > self.speed:
            angle = atan(self.joystickY/self.joystickX)
            if angle < 0:
                angle = 2 * pi + angle
            
            if self.joystickX > 0:
                self.speedX = self.speed * cos(angle)
                self.speedY = self.speed * sin(angle)
            else:
                self.speedX = -self.speed * cos(angle)
                self.speedY = -self.speed * sin(angle) 

        else:
            self.speedX = self.joystickX * self.speed
            self.speedY = self.joystickY * self.speed

        if abs(self.joystickX) - self.joystickDeadzone > 0 or abs(self.joystickY) - self.joystickDeadzone > 0:
            self.moved = True


    def rumble(self, dt, boost = 0, asteroid = False, powerup = False):
        if self.firstPress:
            self.boosting = True
            self.controller.rumble(0.5, 0, 0)

        if self.released or (self.boosting and boost <= 0):
            self.boosting = False
            self.controller.stop_rumble()
        
        if asteroid:
            self.controller.rumble(1, 1, 200)
        
        if powerup:
            self.powerupRumble = True
            self.lastRumble = 0

        if self.powerupRumble:
            self.lastRumble += dt * 1000
            if self.lastRumble >= self.powerupRumbleCount * 100:
                self.controller.rumble(0.8, 0.8, 50)
                self.powerupRumbleCount += 1
            if self.powerupRumbleCount > 3:
                self.powerupRumbleCount = 0
                self.powerupRumble = False