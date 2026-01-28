import pygame
import math as m
import classes as c
import pandas as pd
pygame.init()

# function to find the size of a tile, given the number of rows, columns, and size of the screen
def findSize(screen, rows, cols):
    screenWidth = screen.get_width()
    screenHeight = screen.get_height()
    size = min(screenHeight/rows, screenWidth/cols)
    return m.floor(size/2) * 2 # to allow for tiles to have an even size, needed for centering
# Creates or updates the screen, to allow for fullscreen
def createScreen(width, height, fullscreen = False):
    if fullscreen:
        screen = pygame.display.set_mode((width, height), flags=pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
    return screen
def getPlayerAndEnemyInformation():
    playerInformation = []
    enemyInformation = []
    df = pd.read_csv("agent_information.csv")
    for row in df.iterrow():
        if row['char_label'] == 'medic':
            playerInformation.append(c.MEDIC(row['health_points'], row['base_attack'], row['attack_range'], row['move_speed'], pygame.math.Vector2(0, 0), f"{row['char_label']}Proto"))
        elif row['player_agent']:
            playerInformation.append(c.PLAYER(row['health_points'], row['base_attack'], row['attack_range'], row['move_speed'], pygame.math.Vector2(0, 0), f"{row['char_label']}Proto"))
        else:
            enemyInformation.append(c.ENEMY(row['health_points'], row['base_attack'], row['attack_range'], row['move_speed'], pygame.math.Vector2(0, 0), f"{row['char_label']}Proto"))
    return playerInformation, enemyInformation
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
# Initialise the grid, temporarily has a set size.
rows = 4
cols = 5
size = findSize(screen, rows, cols)
top = (screenHeight - (size * rows)) // 2
left = (screenWidth - (size * cols)) // 2
tiles = [[c.TILE(size, row, col, left + (col * size), top + (row * size), "tile") for col in range(cols)] for row in range(rows)]
# Get player and enemy information
playerInfo, enemyInfo = getPlayerAndEnemyInformation
# Temporary: Assign each player a set position, PLAYER COPYING IS NEEDED STILL
players = []
rowPlace = 0
for player in playerInfo:
    playerForLevel = player.copySelf()
    playerForLevel.updatePosition(pygame.math.Vector2(0, rowPlace))
    players.append(playerForLevel)
    rowPlace += 1
# Initialise enemies as nothing, as no enemy agent information yet. This will eventually be loaded from the level information
enemies = []
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
    # HP Rendered after everything else rendered, to allow it to be shown on top of everything else
    # Render HP of all player agents
    for player in players:
        player.renderHP(screen, tiles)
    # Render HP of all enemy agents
    for enemy in enemies:
        enemy.renderHP(screen, tiles)
    pygame.display.flip()
    # Update time and frame
    dt = clock.tick(30)
    frame = (frame + 1) % framesPerCycle
pygame.quit()