import pygame
import math
import classes as c
pygame.init()

# function to find the size of a tile, given the number of rows, columns, and size of the screen
def findSize(screen, rows, cols):
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()
    size = min(screenHeight/rows, screenWidth/cols)
    return math.floor(size/2) * 2 # to allow for tiles to have an even size, needed for centering
# Creates or updates the screen, to allow for fullscreen
def createScreen(width, height, fullscreen = False):
    if fullscreen:
        screen = pygame.display.set_mode((width, height), flags=pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
    return screen
# Get monitor size
monitorInfo = pygame.display.Info()
monitorWidth, monitorHeight = monitorInfo.current_w, monitorInfo.current_h

# Initialise screen
screenWidth = monitorWidth//2
screenHeight = monitorHeight//2
screen = createScreen(screenWidth, screenHeight)
fullscreen = False
oldWidth = screenWidth
oldHeight = screenHeight
# Load the assets. All assets should be 32 x 32 pixels big
image = pygame.image.load("assets/tile.png")

# Initialise the grid, temporarily has a set size.
rows = 4
cols = 5
size = findSize(screen, rows, cols)
top = (screenHeight - (size * rows)) // 2
left = (screenWidth - (size * cols)) // 2
tiles = [[c.TILE(size, row, col, left + (col * size), top + (row * size), image) for col in range(cols)] for row in range(rows)]
# Temporary: Initialise player and enemy, for testing of rendering
players = [c.PLAYER(1, 1, 1, 1, pygame.math.Vector2(0, i)) for i in range(3)]
enemies = [c.ENEMY(1, 1, 1, 1, pygame.math.Vector2(cols - 1, i + 1)) for i in range(3)]
# Time
clock = pygame.time.Clock()
dt = 0
frame = 0

# Frames per cycle: number of frames per animation cycle
framesPerCycle = 8

# game loop
running = True
while running:
    updateSize = False
    # Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWSIZECHANGED:
            screenWidth = screen.get_width()
            screenHeight = screen.get_height()
            size = findSize(screen, rows, cols)
            updateSize = True
        # TEMP: fullscreen adjustment
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                fullscreen = not(fullscreen)
                if fullscreen:
                    oldWidth = screenWidth
                    oldHeight = screenHeight
                    screen = createScreen(monitorWidth, monitorHeight, fullscreen)
                else:
                    screen = createScreen(oldWidth, oldHeight, fullscreen)
                size = findSize(screen, rows, cols)
                updateSize = True
    # Display
    screen.fill("white")
    # Render tiles
    for row in tiles:
        for col in row:
            if updateSize:
                col.updateSizeAndPos(size, screenWidth, screenHeight, rows, cols)
            col.render(screen)
    # Render player agents
    for player in players:
        player.render(screen, tiles)
    # Render enemy agents
    for enemy in enemies:
        enemy.render(screen, tiles)
    pygame.display.flip()
    # Update time and frame
    dt = clock.tick(30)
    frame = (frame + 1) % framesPerCycle
pygame.quit()