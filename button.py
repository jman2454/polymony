import pygame
from constants import Config

class Button:
    def __init__(self, pos=Config.SCREEN_CENTER, size=(Config.SCREEN_WIDTH/8, Config.SCREEN_HEIGHT/20), color=Config.WHITE, callback=None):
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.callback = callback

    def update(self, evt):
        assert evt.type == pygame.MOUSEBUTTONDOWN
        if self.rect.collidepoint(evt.pos):
            if self.callback:
                self.callback()

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, self.rect)
        pygame.draw.rect(canvas, Config.BLACK, self.rect, width=3)