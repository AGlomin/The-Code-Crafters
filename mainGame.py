import pygame
import math as m
import classes as c
import pandas as pd
import LevelHandler
import time
import uuid
from Telemetry.telemetry.logger import log_event
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
    for row in df.itertuples():
        if row.char_label == 'medic':
            playerInformation.append(c.MEDIC(row.health_points, row.base_attack, row.attack_range, row.move_speed, pygame.math.Vector2(0, 0), f"{row.char_label}Proto", row.char_label))
        elif row.player_agent:
            playerInformation.append(c.PLAYER(row.health_points, row.base_attack, row.attack_range, row.move_speed, pygame.math.Vector2(0, 0), f"{row.char_label}Proto", row.char_label))
        else:
            enemyInformation.append(c.ENEMY(row.health_points, row.base_attack, row.attack_range, row.move_speed, pygame.math.Vector2(0, 0), f"{row.char_label}Proto", row.char_label))
    return playerInformation, enemyInformation
def loadEnemies(enemyInfo, stageEnemies):
    enemies = []
    for enemyLoad in stageEnemies:
        enemyLabel = enemyLoad[0]
        enemyRow = enemyLoad[1]
        enemyCol = enemyLoad[2]
        for enemyCheck in enemyInfo:
            if enemyCheck.checkLabel(enemyLabel):
                e = enemyCheck.copySelf()
                e.updatePosition(pygame.math.Vector2(enemyCol, enemyRow))
                enemies.append(e)
                break
    return enemies
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
"""
rows = 4
cols = 5
"""
rows, cols, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol, obstaclePlaces, stages = LevelHandler.loadLevel("levels/levelTest.txt")
playerPlaces = [[brawlerRow, brawlerCol], [bomberRow, bomberCol], [medicRow, medicCol]]
size = findSize(screen, rows, cols)
top = (screenHeight - (size * rows)) // 2
left = (screenWidth - (size * cols)) // 2
tiles = [[c.TILE(size, row, col, left + (col * size), top + (row * size), "tile") for col in range(cols)] for row in range(rows)]
# Get player and enemy information
playerInfo, enemyInfo = getPlayerAndEnemyInformation()
# Temporary: Assign each player a set position, PLAYER COPYING IS NEEDED STILL
players = []
rowPlace = 0
for player in playerInfo:
    playerForLevel = player.copySelf()
    playerForLevel.updatePosition(pygame.math.Vector2(playerPlaces[rowPlace][1], playerPlaces[rowPlace][0]))
    players.append(playerForLevel)
    rowPlace += 1
# Initialise enemies as nothing, as no enemy agent information yet. This will eventually be loaded from the level information
enemies = loadEnemies(enemyInfo, stages[0])
#add 1 enemy if there are no enemies already so stage_completes can trigger
if len(enemies) == 0 and len(enemyInfo) > 0:
    e = enemyInfo[0].copySelf()
    e.updatePosition(pygame.math.Vector2(cols - 1, 0))
    enemies.append(e)
#stage identifier
stage_id = 1

# Turn-based state
turn_number = 1
active_side = "player"  # "player" or "enemy"
stage_running = True

# Optional stage metric (expand later)
total_damage_taken = 0

# Emit session + stage start events
log_event(
    "session_start",
    stage_id,
    {
        "config_id": "balanced",
        "difficulty_label": "balanced"
    }
)

log_event(
    "stage_start",
    stage_id,
    {
        "enemy_count": len(enemies),
        "grid_size": f"{rows}x{cols}"
    }
)

log_event(
    "turn_start",
    stage_id,
    {
        "turn_number": turn_number,
        "active_side": active_side
    }
)

def get_hp(agent):
    #Supports different attribute names (adjust if your classes differ)
    if hasattr(agent, "health_points"):
        return agent.health_points
    if hasattr(agent, "hp"):
        return agent.hp
    return 1

def stage_won(enemies):
    #Win: all enemies defeated (requires at least 1 enemy)
    return len(enemies) > 0 and all(get_hp(e) <= 0 for e in enemies)

def stage_lost(players):
    #Fail: all players defeated
    return all(get_hp(p) <= 0 for p in players)

def advance_turn():
    global active_side, turn_number
    if active_side == "player":
        active_side = "enemy"
    else:
        active_side = "player"
        turn_number += 1
        
#Time
clock = pygame.time.Clock()
dt = 0
frame = 0

#Frames per cycle: number of frames per animation cycle
framesPerCycle = 8

#game loop
running = True
while running:
    updateSize = False
    # Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if stage_running:
                log_event(
                    "quit",
                    stage_id,
                    {
                        "turn_number": turn_number
                    }
                )
                log_event(
                    "stage_fail",
                    stage_id,
                    {
                        "turns_taken": turn_number,
                        "failure_reason": "window_closed"
                    }
                )
                log_event(
                    "session_end",
                    stage_id,
                    {
                        "stages_completed": 0
                    }
                )
            running = False
        if event.type == pygame.WINDOWSIZECHANGED:
            screenWidth = screen.get_width()
            screenHeight = screen.get_height()
            size = findSize(screen, rows, cols)
            updateSize = True
            
            
        #TEMP: fullscreen adjustment
        if event.type == pygame.KEYUP:
            # debugger: press W to force win (sets all enemies HP to 0)
            if event.key == pygame.K_w and stage_running:
                for enemy in enemies:
                    if hasattr(enemy, "health_points"):
                        enemy.health_points = 0
                    elif hasattr(enemy, "hp"):
                        enemy.hp = 0
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
            #advance turn by pressing SPACEBAR
            if event.key == pygame.K_SPACE and stage_running:
                advance_turn()
                log_event(
                    "turn_start",
                    stage_id,
                    {
                        "turn_number": turn_number,
                        "active_side": active_side
                    }
                )
            #quit mid-stage by pressing ESC
            if event.key == pygame.K_ESCAPE and stage_running:
                stage_running = False
                log_event(
                    "quit",
                    stage_id,
                    {
                        "turn_number": turn_number
                    }
                )
                log_event(
                    "stage_fail",
                    stage_id,
                    {
                        "turns_taken": turn_number,
                        "failure_reason": "quit"
                    }
                )
                log_event(
                    "session_end",
                    stage_id,
                    {
                        "stages_completed": 0
                    }
                )
                running = False
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
    #stage-end conditions (succeed/fail)
    if stage_running:
        if stage_won(enemies):
            stage_running = False
            log_event(
                "stage_complete",
                stage_id,
                {
                    "turns_taken": turn_number,
                    "characters_alive": sum(1 for p in players if get_hp(p) > 0),
                    "total_damage_taken": total_damage_taken
                }
            )
            log_event(
                "session_end",
                stage_id,
                {
                    "stages_completed": 1
                }
            )
            running = False
    
        elif stage_lost(players):
            stage_running = False
            log_event(
                "stage_fail",
                stage_id,
                {
                    "turns_taken": turn_number,
                    "failure_reason": "all_players_defeated"
                }
            )
            log_event(
                "session_end",
                stage_id,
                {
                    "stages_completed": 0
                }
            )
            running = False

    # Update time and frame
    dt = clock.tick(30)
    frame = (frame + 1) % framesPerCycle

pygame.quit()

