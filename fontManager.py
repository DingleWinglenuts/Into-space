import pygame

# This file creates an object that contains a dictionary for fonts and allows for easy rendering of these fonts

class FontManager():
    def __init__(self):
        self.fonts = {}

    def add(self, font = pygame.font.Font, identifier = str): # Adds a new font to the dictionary (and raises an error if the key used for this font is already in the dictionary)
        if identifier in self.fonts:
            raise KeyError("Existing font with name " + identifier + ". Use different identifier.")
        self.fonts[identifier] = font
    
    def render(self, identifier = str, txt = str, colour = tuple): # Creates a text image based on a selected font (and raises an error if the font identifier doesnt exist)
        if identifier not in self.fonts:
            raise KeyError("No font named " + identifier + " exists. Add font first.")
        msg = self.fonts[identifier].render(txt, True, colour)
        return msg
