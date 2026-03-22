import pygame
import math as m
import classes as c
import pandas as pd
import LevelHandler
import time
import uuid
from Telemetry.telemetry.logger import log_event
import json
import os

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARAMS_PATH = os.path.join(BASE_DIR, "balancing_toolkit", "parameters.json")
LEVELS_DIR = os.path.join(BASE_DIR, "levels")
AGENT_INFO_PATH = os.path.join(BASE_DIR, "agent_information.csv")

with open(PARAMS_PATH, "r", encoding="utf-8") as f:
    params = json.load(f)

pygame.init()

# FOR TESTING
session_id = "0 but a string"
user_id = "1 but a string"


# Creates or updates the screen, to allow for fullscreen
def createScreen(width, height, fullscreen=False):
    if fullscreen:
        screen = pygame.display.set_mode((width, height), flags=pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
    return screen


# Difficulty Modifier. 0 = easy, 1 = normal, 2 = hard
def playLevel(levelNumber, difficulty, screen, fullscreen, oldWidth, oldHeight, monitorWidth, monitorHeight):
    doHide = False
    levelCompleted = False
    difficultyAtkChange = params["level" + str(levelNumber)]["difficultyAttackScaling"]
    difficultyModifier = 1 + (difficultyAtkChange * (difficulty - 1))

    # function to find the size of a tile, given the number of rows, columns, and size of the screen
    def findSize(screen, rows, cols):
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        size = min(screenHeight / rows, screenWidth / cols)
        return m.floor(size / 2) * 2

    def getPlayerAndEnemyInformation(difficultyMod):
        applyParamChange = True
        playerInformation = []
        enemyInformation = []
        df = pd.read_csv(AGENT_INFO_PATH)

        for row in df.itertuples():
            # Default changes
            player_health = 0
            player_attack = 0
            player_range = 0
            player_speed = 0

            enemy_health = 0
            enemy_attack = 0
            enemy_range = 0
            enemy_speed = 0

            if applyParamChange:
                level_key = "level" + str(levelNumber)

                if row.player_agent:
                    player_key = row.char_label
                    player = params[level_key].get(
                        player_key,
                        {
                            "health": 0,
                            "attack": 0,
                            "attack_range": 0,
                            "move_speed": 0,
                        },
                    )

                    player_health += player["health"]
                    player_attack += player["attack"]
                    player_range += player["attack_range"]
                    player_speed += player["move_speed"]

                else:
                    enemy_key = row.char_label
                    enemy = params[level_key].get(
                        enemy_key,
                        {
                            "health": 0,
                            "attack": 0,
                            "attack_range": 0,
                            "move_speed": 0,
                        },
                    )

                    enemy_health += enemy["health"]
                    enemy_attack += enemy["attack"]
                    enemy_range += enemy["attack_range"]
                    enemy_speed += enemy["move_speed"]

            if row.char_label == "medic":
                agentHP = max(1, row.health_points + player_health)
                agentAttack = max(1, row.base_attack + player_attack)
                agentRange = max(1, row.attack_range + player_range)
                agentSpeed = max(1, row.move_speed + player_speed)
                playerInformation.append(
                    c.MEDIC(
                        agentHP,
                        agentAttack,
                        agentRange,
                        agentSpeed,
                        pygame.math.Vector2(0, 0),
                        "medic",
                        row.char_label,
                    )
                )

            elif row.player_agent:
                agentHP = max(1, row.health_points + player_health)
                agentAttack = max(1, row.base_attack + player_attack)
                agentRange = max(1, row.attack_range + player_range)
                agentSpeed = max(1, row.move_speed + player_speed)
                playerInformation.append(
                    c.PLAYER(
                        agentHP,
                        agentAttack,
                        agentRange,
                        agentSpeed,
                        pygame.math.Vector2(0, 0),
                        f"{row.char_label}",
                        row.char_label,
                    )
                )

            else:
                agentHP = max(1, row.health_points + enemy_health)
                agentAttack = max(1, row.base_attack + enemy_attack)
                agentRange = max(1, row.attack_range + enemy_range)
                agentSpeed = max(1, row.move_speed + enemy_speed)
                sprite_name = "en0" if row.char_label == "en0" else f"{row.char_label}Proto"
                enemyInformation.append(
                    c.ENEMY(
                        agentHP,
                        agentAttack,
                        agentRange,
                        agentSpeed,
                        pygame.math.Vector2(0, 0),
                        sprite_name,
                        row.char_label,
                        difficultyMod,
                    )
                )

        return playerInformation, enemyInformation

    def loadEnemies(enemyInfo, stageEnemies, stageWidth, stageHeight, players):
        enemies = []
        enemyLabels = {}
        for enemyLoad in stageEnemies:
            enemyLabel = enemyLoad[0]
            enemyRow = enemyLoad[1]
            enemyCol = enemyLoad[2]
            for enemyCheck in enemyInfo:
                if enemyCheck.checkLabel(enemyLabel):
                    if enemyLabel in enemyLabels.keys():
                        enemyLabels[enemyLabel] += 1
                    else:
                        enemyLabels[enemyLabel] = 0
                    e = enemyCheck.copySelf()
                    e.updatePosition(pygame.math.Vector2(enemyCol, enemyRow))
                    e.fixSpawn(stageWidth, stageHeight, obstacles, players, enemies)
                    e.getBaseFacingDir(stageWidth)
                    e.setLabel(f"{enemyLabel}.{enemyLabels[enemyLabel]}")
                    enemies.append(e)
                    break
        return enemies

    # Get active player from those still alive
    def getActiveFromAlive(players, currActive):
        for i in range(len(players)):
            if players[currActive].findAlive() == 1:
                return currActive
            currActive = (currActive + 1) % len(players)
        return currActive

    level_path = os.path.join(LEVELS_DIR, f"level{levelNumber}.txt")
    rows, cols, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol, obstaclePlaces, stages = LevelHandler.loadLevel(level_path)

    playerPlaces = [[brawlerRow, brawlerCol], [bomberRow, bomberCol], [medicRow, medicCol]]
    size = findSize(screen, rows, cols)
    screenWidth, screenHeight = screen.get_width(), screen.get_height()
    top = (screenHeight - (size * rows)) // 2
    left = (screenWidth - (size * cols)) // 2
    tiles = [[c.TILE(size, row, col, left + (col * size), top + (row * size), "tile") for col in range(cols)] for row in range(rows)]
    obstacles = [c.OBSTACLE(pygame.math.Vector2(obstacle[1], obstacle[0]), "obstacle") for obstacle in obstaclePlaces]

    # Get player and enemy information
    playerInfo, enemyInfo = getPlayerAndEnemyInformation(difficultyModifier)

    # Assign each player a set position
    players = []
    rowPlace = 0
    for player in playerInfo:
        playerForLevel = player.copySelf()
        playerForLevel.updatePosition(pygame.math.Vector2(playerPlaces[rowPlace][1], playerPlaces[rowPlace][0]))
        players.append(playerForLevel)
        rowPlace += 1

    # stage identifier
    level_id = 0
    stage_id = 0

    def loadStage(stage_id, stages, enemyInfo):
        global enemies
        enemies = loadEnemies(enemyInfo, stages[stage_id], cols, rows, players)

        # add 1 enemy if there are no enemies already so stage_complete can trigger correctly later
        if len(enemies) == 0 and len(enemyInfo) > 0:
            e = enemyInfo[0].copySelf()
            e.updatePosition(pygame.math.Vector2(cols - 1, 0))
            e.fixSpawn(cols, rows, obstacles, players, enemies)
            e.getBaseFacingDir(cols)
            enemies.append(e)
        return enemies

    enemies = loadStage(stage_id, stages, enemyInfo)

    # Turn-based state
    turn_number = 1
    active_side = "player"
    stage_running = True

    total_damage_taken = 0

    # Emit session + stage start events
    log_event(
        "session_start",
        level_id,
        stage_id,
        session_id,
        user_id,
        {
            "session_id": session_id,
            "config_id": "balanced",
            "difficulty_label": "balanced",
        },
    )

    log_event(
        "level_start",
        level_id,
        stage_id,
        session_id,
        user_id,
        {
            "session_id": session_id,
            "grid_size": f"{rows}x{cols}",
        },
    )

    log_event(
        "stage_start",
        level_id,
        stage_id,
        session_id,
        user_id,
        {
            "session_id": session_id,
            "enemy_count": len(enemies),
            "grid_size": f"{rows}x{cols}",
        },
    )

    log_event(
        "turn_start",
        level_id,
        stage_id,
        session_id,
        user_id,
        {
            "session_id": session_id,
            "turn_number": turn_number,
            "active_side": active_side,
        },
    )

    def stage_won(enemies):
        return (len(enemies) > 0 and all(e.findAlive() == 0 for e in enemies)) or len(enemies) == 0

    def stage_lost(players):
        return all(p.findAlive() == 0 for p in players)

    def advance_turn(active_side, turn_number):
        if active_side == "player":
            active_side = "enemy"
        else:
            active_side = "player"
            turn_number += 1
        return active_side, turn_number

    def logAttack(agent, isPlayer, targets):
        agentLabel = agent.getLabel()
        agentDamage = agent.getAttack()
        agentRange = agent.getAttackRange()
        for target in targets:
            if isPlayer:
                if agentLabel == "medic":
                    log_event(
                        "character_heal",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {
                            "healer_id": agentLabel,
                            "target_id": target,
                            "heal_amount": agentDamage,
                            "healing_range": agentRange,
                        },
                    )
                else:
                    log_event(
                        "character_attack",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {
                            "session_id": session_id,
                            "attacker_id": agentLabel,
                            "target_id": target,
                            "damage": agentDamage,
                            "attack_range": agentRange,
                        },
                    )
            else:
                log_event(
                    "enemy_attack",
                    level_id,
                    stage_id,
                    session_id,
                    user_id,
                    {
                        "session_id": session_id,
                        "enemy_id": agentLabel,
                        "target_id": target,
                        "damage": agentDamage,
                    },
                )

    # Time
    clock = pygame.time.Clock()
    dt = 0
    frame = 0
    frameModifier = 0.125
    actualFrame = 0
    moveFrame = 0
    damageFrame = 0
    framesPerDamage = 16
    animating = False
    animatingMove = False
    movementDone = False
    damageLogged = False

    running = True
    activePlayer = 0

    # Start players
    for player in players:
        player.startTurn(cols, rows, obstacles, players, enemies)
        player.getBaseFacingDir(cols)

    while running:
        updateSize = False

        # Checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if stage_running:
                    log_event(
                        "quit",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {
                            "session_id": session_id,
                            "turn_number": turn_number,
                        },
                    )
                    log_event(
                        "stage_fail",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {
                            "session_id": session_id,
                            "turns_taken": turn_number,
                            "failure_reason": "window_closed",
                        },
                    )
                    log_event(
                        "session_end",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {
                            "session_id": session_id,
                            "stages_completed": (3 * level_id + stage_id),
                        },
                    )
                running = False

            if event.type == pygame.WINDOWSIZECHANGED:
                screenWidth = screen.get_width()
                screenHeight = screen.get_height()
                size = findSize(screen, rows, cols)
                updateSize = True

            if event.type == pygame.MOUSEBUTTONUP:
                if active_side == "player" and not animating:
                    mx, my = event.pos
                    clickedRow, clickedCol = -1, -1
                    for row in tiles:
                        for col in row:
                            selectedRow, selectedCol = col.getClicked(mx, my)
                            if selectedRow != -1 and selectedCol != -1:
                                clickedRow = selectedRow
                                clickedCol = selectedCol

                    if clickedRow == -1 and clickedCol == -1:
                        continue

                    # Check if clicking a player
                    playerClicked = False
                    for playerI in range(len(players)):
                        if not playerClicked:
                            player = players[playerI]
                            playerPos, _ = player.getPositions()
                            if playerPos.x == clickedCol and playerPos.y == clickedRow and activePlayer != playerI and player.findAlive() == 1:
                                playerClicked = True
                                activePlayer = playerI

                    if playerClicked:
                        continue

                    moveSuccessful = players[activePlayer].attemptToMove(clickedRow, clickedCol, players)

                    if moveSuccessful:
                        for player in players:
                            player.getMoveableLocations(cols, rows, obstacles, players, enemies, False)
                        for enemy in enemies:
                            enemy.getMoveableLocations(cols, rows, obstacles, players, enemies)

            if event.type == pygame.KEYUP:
                # debugger: press W to force win
                if event.key == pygame.K_w and stage_running:
                    for enemy in enemies:
                        enemy.setHP(0)

                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        oldWidth = screenWidth
                        oldHeight = screenHeight
                        screen = createScreen(monitorWidth, monitorHeight, fullscreen)
                    else:
                        screen = createScreen(oldWidth, oldHeight, fullscreen)
                    size = findSize(screen, rows, cols)
                    updateSize = True

                # advance turn by pressing SPACEBAR
                if event.key == pygame.K_SPACE and stage_running:
                    animating = True
                    animatingMove = True
                    if active_side == "player":
                        for player in players:
                            player.getMoveableLocations(cols, rows, obstacles, players, enemies, False)
                            player.getMovementPath()
                            moveFrame = 0

                # quit mid-stage by pressing ESC
                if event.key == pygame.K_ESCAPE and stage_running:
                    stage_running = False
                    log_event(
                        "quit",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {
                            "session_id": session_id,
                            "turn_number": turn_number,
                        },
                    )
                    log_event(
                        "stage_fail",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {
                            "session_id": session_id,
                            "turns_taken": turn_number,
                            "failure_reason": "quit",
                        },
                    )
                    log_event(
                        "session_end",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {
                            "session_id": session_id,
                            "stages_completed": (3 * level_id + stage_id),
                        },
                    )
                    running = False

        if animating:
            animatingAgents = players if active_side == "player" else enemies

            # Animate Movement
            if animatingMove:
                if all([agent.getMovesLeft() == 0 for agent in animatingAgents]):
                    movementDone = True

                if movementDone:
                    for agent in animatingAgents:
                        agent.updatePosition(agent.getMoveTo())

                    for player in players:
                        player.getMoveableLocations(cols, rows, obstacles, players, enemies)
                    for enemy in enemies:
                        enemy.getMoveableLocations(cols, rows, obstacles, players, enemies)

                    animatingMove = False

            # Animate Attack
            else:
                if damageLogged:
                    damageFrame += 1
                    if damageFrame == framesPerDamage:
                        for player in players:
                            player.matchCurrToPrevHP()

                        enemiesAfterTurn = []
                        for enemy in enemies:
                            enemy.matchCurrToPrevHP()
                            if enemy.findAlive() == 1:
                                enemiesAfterTurn.append(enemy)

                        enemies = enemiesAfterTurn.copy()
                        damageLogged = False
                        animating = False
                        movementDone = False
                        animatingMove = True

                        log_event(
                            "turn_end",
                            level_id,
                            stage_id,
                            session_id,
                            user_id,
                            {
                                "session_id": session_id,
                                "turn_number": turn_number,
                                "active_side": active_side,
                            },
                        )

                        active_side, turn_number = advance_turn(active_side, turn_number)

                        log_event(
                            "turn_start",
                            level_id,
                            stage_id,
                            session_id,
                            user_id,
                            {
                                "session_id": session_id,
                                "turn_number": turn_number,
                                "active_side": active_side,
                            },
                        )

                        if active_side == "enemy":
                            for enemy in enemies:
                                enemy.findOptimalMoveLocation(cols, rows, obstacles, players, enemies)
                                enemy.getMoveableLocations(cols, rows, obstacles, players, enemies, False)
                                enemy.getMovementPath()
                                moveFrame = 0
                            animating = True
                            for player in players:
                                player.endTurn()
                        else:
                            activePlayer = getActiveFromAlive(players, activePlayer)
                            for player in players:
                                player.startTurn(cols, rows, obstacles, players, enemies)

                else:
                    for agent in animatingAgents:
                        if agent.findAlive() == 1:
                            if active_side == "player" and agent.getLabel() != "medic":
                                targets = agent.attack(enemies)
                                logAttack(agent, True, targets)
                            else:
                                targets = agent.attack(players)
                                logAttack(agent, agent.getLabel() == "medic", targets)

                    damageFrame = 0
                    damageLogged = True

        # stage-end conditions
        if stage_running:
            if stage_won(enemies):
                log_event(
                    "stage_complete",
                    level_id,
                    stage_id,
                    session_id,
                    user_id,
                    {
                        "session_id": session_id,
                        "turns_taken": turn_number,
                        "characters_alive": sum(p.findAlive() for p in players),
                        "total_damage_taken": total_damage_taken,
                    },
                )

                stage_id += 1
                if stage_id == 3:
                    log_event(
                        "level_complete",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {
                            "session_id": session_id,
                            "characters_alive": sum(p.findAlive() for p in players),
                        },
                    )
                    running = False
                    levelCompleted = True

                else:
                    enemies = loadStage(stage_id, stages, enemyInfo)

                    log_event(
                        "stage_start",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {
                            "session_id": session_id,
                            "enemy_count": len(enemies),
                            "grid_size": f"{rows}x{cols}",
                        },
                    )
                    active_side = "player"
                    turn_number = 1
                    activePlayer = getActiveFromAlive(players, activePlayer)
                    for player in players:
                        player.startTurn(cols, rows, obstacles, players, enemies)
                    animating = False
                    animatingMove = False

            elif stage_lost(players):
                stage_running = False
                log_event(
                    "stage_fail",
                    level_id,
                    stage_id,
                    session_id,
                    user_id,
                    {
                        "session_id": session_id,
                        "turns_taken": turn_number,
                        "failure_reason": "all_players_defeated",
                    },
                )
                log_event(
                    "session_end",
                    level_id,
                    stage_id,
                    session_id,
                    user_id,
                    {
                        "session_id": session_id,
                        "stages_completed": (3 * level_id + stage_id),
                    },
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

        # Render players
        for playerI, player in enumerate(players):
            showRender = player.findAlive() == 1 or not doHide
            player.render(
                screen,
                tiles,
                actualFrame,
                moveFrame,
                showRender,
                active_side == "player" and not animating and player.findAlive() == 1,
                True,
                activePlayer == playerI,
            )

        # Render enemies
        for enemy in enemies:
            enemy.render(screen, tiles, actualFrame, moveFrame, True)

        # Render obstacles
        for obstacle in obstacles:
            obstacle.render(screen, tiles)

        # Render HP
        for player in players:
            showRender = player.findAlive() == 1
            player.renderHP(screen, tiles, moveFrame, damageFrame, showRender)

        for enemy in enemies:
            enemy.renderHP(screen, tiles, moveFrame, damageFrame, True)

        pygame.display.flip()

        dt = clock.tick(30)
        frame = frame + frameModifier
        actualFrame = m.floor(frame)
        moveFrame += 1

    return levelCompleted


if __name__ == '__main__':
    # Get monitor size
    monitorInfo = pygame.display.Info()
    monitorWidth, monitorHeight = monitorInfo.current_w, monitorInfo.current_h

    # Initialise screen
    screenWidth = monitorWidth // 2
    screenHeight = monitorHeight // 2
    screen = createScreen(screenWidth, screenHeight)
    fullscreen = False
    oldWidth = screenWidth
    oldHeight = screenHeight

    for levelNum in range(2):
        playLevel(levelNum, 0, screen, fullscreen, oldWidth, oldHeight, monitorWidth, monitorHeight)