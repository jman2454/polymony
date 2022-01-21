import pygame
from constants import Config

class DiscreteSlider:

    def __init__(self, count, pos, size, padding_pct=.05, label_fn=None, callback=None):
        self.size = size
        self.pos = pos
        self.count = count
        self.rect = pygame.Rect(pos, size)
        self.dragging = False
        self.selection = 0
        self.padding = padding_pct * self.size[0]
        self.callback = callback

    def getSelection(self):
        return self.selection

    def update(self, evt):
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(evt.pos):
                self.select(evt.pos)
                self.dragging = True
        elif evt.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif evt.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.select(evt.pos)

    def draw(self, canvas):
        pygame.draw.rect(canvas, Config.RED, self.rect, border_radius=int(self.size[0] / 2))
        for i in range(self.count): 
            fill_color = Config.WHITE

            if self.selection - 1 == i:
                fill_color = Config.BLACK
            r = self.size[0] / (self.count * 3)
            pygame.draw.circle(canvas, fill_color, 
                (self.pos[0] + (self.padding / 2) + i * (self.size[0] - self.padding)/self.count + r/2, self.pos[1] + self.size[1]/2), 
                r)

    def select(self, pos):
        self.pct = min(max((pos[0] - (Config.SCREEN_WIDTH - self.size[0] + self.padding)/2)/(self.size[0] - self.padding), .01), 1)
        orig = self.selection
        self.selection = 1 + round(self.count * self.pct)
        if self.selection != orig:
            self.callback(self.selection)