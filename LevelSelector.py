import pygame

class RecyclerView:
    def __init__(self, renderRect, itemWidth):
        self.renderRect = renderRect
        self.items = []
        self.index = 0
        self.t = float(1)
        self.fittableItems = renderRect.width // itemWidth + 2
        self.itemWidth = itemWidth
    def populate(self, items):
        for item in items:
            self.items.append(self.RecyclerViewItem(item, self.itemWidth))
    def addItem(self, item, index = -1):
        if index == -1:
            self.items.append(self.RecyclerViewItem(item, self.itemWidth))
        else:
            self.items.insert(index, self.RecyclerViewItem(item, self.itemWidth))
    def removeItem(self, index):
        self.items.pop(index)
    def render(self, screen):
        renderSurface = pygame.Surface(self.renderRect.size, flags = pygame.SRCALPHA)
        for i in range(self.fittableItems):
            itemIndex = i + self.index
            if itemIndex < len(self.items):
                self.items[itemIndex].render(renderSurface, self.t, i)
        screen.blit(renderSurface, self.renderRect)
    def setT(self, t):
        self.t = t
    def changeT(self, amount):
        self.t += amount
        if self.t < 0:
                self.t += 1
                if self.changeIndex(1):
                    self.t = 0
        if self.t > 1:
            self.t -= 1
            if self.changeIndex(-1):
                self.t = 1
    def changeIndex(self, amount):
        self.index += amount
        changed = False
        if self.index < 0:
            self.index = 0
            changed = True
        if self.index > len(self.items) - self.fittableItems + 1:
            self.index = len(self.items) - self.fittableItems + 1
            changed = True
        return changed
    # for testing
    def getT(self):
        return self.t
    def getIndex(self):
        return self.index
    class RecyclerViewItem:
        def __init__(self, content, width):
            self.content = content
            self.width = width
        def render(self, surface, t, indexFromStart):
            x = (t + indexFromStart - 1) * self.width
            imageResized = pygame.transform.scale(self.content, (self.width, surface.get_height()))
            surface.blit(imageResized, (x, 0))