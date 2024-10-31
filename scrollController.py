import pygame

# The object in this file handles the scrolling background and also contains a function to display the background without scrolling (used for the pause menu)

class Scroll():
    def __init__(self, BG, WIN):
        self.scroll = 0
        self.bg = BG
        self.h = BG.get_height()
        self.WIN = WIN

    def scrollBG(self, dt): # Displays and scrolls the background when called
        for i in range(2):
            self.WIN.blit(self.bg, (0, - (i * self.h - self.scroll)))
        
        self.scroll += 20 * dt/(dt + 1)

        if self.scroll > self.h:
            self.scroll = 0

    def idleBlit(self): # Displays the background without scrolling
        for i in range(2):
            self.WIN.blit(self.bg, (0, - (i * self.h - self.scroll)))
