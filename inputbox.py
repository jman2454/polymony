import pygame
from constants import Config

class InputBox:
    def __init__(self, pos=Config.SCREEN_CENTER, size=(Config.SCREEN_WIDTH/8, Config.SCREEN_HEIGHT/20)):
        self.size = size
        self.rect = pygame.Rect(pos, size)

    def handleClick(self, evt):
        assert evt.type == pygame.MOUSEBUTTONDOWN

    def draw(self, canvas):
        pygame.draw.rect(canvas, Config.WHITE, self.rect)
        pygame.draw.rect(canvas, Config.BLACK, self.rect, width=1)

    