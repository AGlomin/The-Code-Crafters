import pygame

# Tile Class: Stores size, row, column, x, y and picture
class TILE:
    def __init__(self, size, row, col, x, y, img):
        self.size = size
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.img = img
    # Render tile to screen
    def render(self, screen):
        rescaledImg = pygame.transform.scale(self.img, (self.size, self.size))
        screen.blit(rescaledImg, (self.x, self.y))
    # Update the size and position of tile, for when screen size is changed
    def updateSizeAndPos(self, size, screenWidth, screenHeight, rows, cols):
        self.size = size
        top = (screenHeight - (size * rows)) // 2
        left = (screenWidth - (size * cols)) // 2
        self.x = left + (self.col * size)
        self.y = top + (self.row * size)
    # Get position, so the player/enemy can access this for movement (less repetition of code)
    def getPosition(self):
        return (self.x, self.y)
# Parent Class: Agent, used as a base for both the player and enemy class
class AGENT:
    def __init__ (self):
        return

# Enemy Class: Class representing an enemy.
class ENEMY(AGENT):
    def __init__ (self):
        super().__init__()
# Player Class: Class representing a player character. NOTE: Medic does NOT use this class, instead uses a child class of player
class PLAYER(AGENT):
    def __init__ (self):
        super().__init__()
# Medic Class: Subclass of Player, to override attack to be a heal
class MEDIC(PLAYER):
    def __init__ (self):
        super().__init__()