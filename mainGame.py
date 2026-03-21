import pygame
import math as m
import classes as c
import pandas as pd
import LevelHandler
import time
import uuid
from Telemetry.telemetry.logger import log_event
import json #for parameters

#To load parameters on to main game.
with open("parameter.json", "r") as f:
    params=json.load(f)
pygame.init()
# FOR TESTING
session_id = "0 but a string"
user_id = "1 but a string"
# Creates or updates the screen, to allow for fullscreen
def createScreen(width, height, fullscreen = False):
    if fullscreen:
        screen = pygame.display.set_mode((width, height), flags=pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
    return screen
# Difficulty Modifier. 0 = easy, 1 = normal, 2 = hard
def playLevel(levelNumber, difficulty, screen, fullscreen, oldWidth, oldHeight, monitorWidth, monitorHeight):
    doHide = False # for testing, can turn this off for showing death animation
    levelCompleted = False
    difficultyAtkChange=params["difficulty"]["attack_scaling"]
    #difficultyAtkChange = 0.25
    difficultyModifier = 1 + (difficultyAtkChange * (difficulty - 1))
    # function to find the size of a tile, given the number of rows, columns, and size of the screen
    def findSize(screen, rows, cols):
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        size = min(screenHeight/rows, screenWidth/cols)
        return m.floor(size/2) * 2 # to allow for tiles to have an even size, needed for centering
    def getPlayerAndEnemyInformation(difficultyMod):
        playerInformation = []
        enemyInformation = []
        df = pd.read_csv("agent_information.csv")
        for row in df.itertuples():

            #load stats from parameters
            player_health=params["player"]["health"]
            player_attack=params["player"]["attack"]
            player_range=params["player"]["attack_range"]
            player_speed=params["player"]["move_speed"]

            enemy_health=params["enemy"]["health"]
            enemy_attack=params["enemy"]["attack"]
            enemy_range=params["enemy"]["attack_range"]
            enemy_speed=params["enemy"]["speed"]

            if row.char_label == 'medic':
                playerInformation.append(c.MEDIC(player_health, player_attack, player_range, player_speed, pygame.math.Vector2(0, 0), f"{row.char_label}", row.char_label))
            elif row.player_agent:
                playerInformation.append(c.PLAYER(row.health_points, row.base_attack, row.attack_range, row.move_speed, pygame.math.Vector2(0, 0), f"{row.char_label}" if row.char_label == "brawler" else f"{row.char_label}Proto", row.char_label))
            else:
                enemyInformation.append(c.ENEMY(enemy_health, enemy_attack, enemy_range, enemy_speed, pygame.math.Vector2(0, 0), f"{row.char_label}Proto", row.char_label, difficultyMod))
        return playerInformation, enemyInformation
        
  #discarded code, greyed out incase new code is wrong.      
            #if row.char_label == 'medic':
                #playerInformation.append(c.MEDIC(row.health_points, row.base_attack, row.attack_range, row.move_speed, pygame.math.Vector2(0, 0), f"{row.char_label}", row.char_label))
            #elif row.player_agent:
                #playerInformation.append(c.PLAYER(row.health_points, row.base_attack, row.attack_range, row.move_speed, pygame.math.Vector2(0, 0), f"{row.char_label}Proto", row.char_label))
            #else:
                #enemyInformation.append(c.ENEMY(row.health_points, row.base_attack, row.attack_range, row.move_speed, pygame.math.Vector2(0, 0), f"{row.char_label}Proto", row.char_label, difficultyMod))
        #return playerInformation, enemyInformation
    
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
    # Get active player from those still alive, defaulting to the last selected, and working through list (closest for list of length 3)
    def getActiveFromAlive(players, currActive):
        for i in range(len(players)):
            if players[currActive].findAlive() == 1:
                return currActive
            currActive = (currActive + 1) % len(players)
        return currActive
    
    # Initialise the grid, temporarily has a set size.
    """
    rows = 4
    cols = 5
    """

    rows, cols, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol, obstaclePlaces, stages = LevelHandler.loadLevel(f"levels/level{levelNumber}.txt")
    playerPlaces = [[brawlerRow, brawlerCol], [bomberRow, bomberCol], [medicRow, medicCol]]
    size = findSize(screen, rows, cols)
    screenWidth, screenHeight = screen.get_width(), screen.get_height()
    top = (screenHeight - (size * rows)) // 2
    left = (screenWidth - (size * cols)) // 2
    tiles = [[c.TILE(size, row, col, left + (col * size), top + (row * size), "tile") for col in range(cols)] for row in range(rows)]
    obstacles = [c.OBSTACLE(pygame.math.Vector2(obstacle[1], obstacle[0]), "obstacle") for obstacle in obstaclePlaces]
    # Get player and enemy information
    playerInfo, enemyInfo = getPlayerAndEnemyInformation(difficultyModifier)
    # Temporary: Assign each player a set position, PLAYER COPYING IS NEEDED STILL
    players = []
    rowPlace = 0
    for player in playerInfo:
        playerForLevel = player.copySelf()
        playerForLevel.updatePosition(pygame.math.Vector2(playerPlaces[rowPlace][1], playerPlaces[rowPlace][0]))
        players.append(playerForLevel)
        rowPlace += 1


    #stage identifier
    level_id = 0
    stage_id = 0

    def loadStage(stage_id, stages, enemyInfo): 
        global enemies
        # Initialise enemies as nothing, as no enemy agent information yet. This will eventually be loaded from the level information
        enemies = loadEnemies(enemyInfo, stages[stage_id], cols, rows, players)
        #add 1 enemy if there are no enemies already so stage_completes can trigger
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
    active_side = "player"  # "player" or "enemy"
    stage_running = True

    # Optional stage metric (expand later)
    total_damage_taken = 0

    # Emit session + stage start events
    log_event(
        "session_start",
        level_id,
        stage_id,
        session_id,
        user_id,
        {   "session_id":session_id,
            "config_id": "balanced",
            "difficulty_label": "balanced"
        }
    )

    log_event(
        "level_start",
        level_id,
        stage_id,
        session_id, 
        user_id,
        {   "session_id":session_id,
            "grid_size": f"{rows}x{cols}"
        }
    )

    log_event(
        "stage_start",
        level_id,
        stage_id,
        session_id,
        user_id,
        {   "session_id":session_id,
            "enemy_count": len(enemies),
            "grid_size": f"{rows}x{cols}"
        }
    )

    log_event(
        "turn_start",
        level_id,
        stage_id,
        session_id,
        user_id,
        {   "session_id":session_id,
            "turn_number": turn_number,
            "active_side": active_side
        }
    )
    """
    def get_hp(agent):
        #Supports different attribute names (adjust if your classes differ)
        if hasattr(agent, "health_points"):
            return agent.health_points
        if hasattr(agent, "hp"):
            return agent.hp
        return 1
    """
    def stage_won(enemies):
        #Win: all enemies defeated (requires at least 1 enemy)
        return (len(enemies) > 0 and all(e.findAlive() == 0 for e in enemies)) or len(enemies) == 0

    def stage_lost(players):
        #Fail: all players defeated
        return all(p.findAlive() == 0 for p in players)

    def advance_turn(active_side, turn_number):
        if active_side == "player":
            active_side = "enemy"
        else:
            active_side = "player"
            turn_number += 1
        return active_side, turn_number
    """
    Dealt with in agent class.
    def damage_agent(agent, amount):
        #reducing hp
        if hasattr(agent, "health_points"):
            agent.health_points = max(0, agent.health_points - amount)
        elif hasattr(agent, "hp"):
            agent.hp = max(0, agent.hp - amount)

    def player_attack():
        if len(enemies) == 0 or len(players) == 0:
            return
        attacker = players[0]
        target = enemies[0]
        damage = 10
        damage_agent(target, damage)
        log_event(
            "character_attack",
            level_id,
            stage_id,
            {
                "attacker_id": getattr(attacker, "name", "player_0"),
                "target_id": getattr(target, "name", "enemy_0"),
                "damage": damage,
                "attack_range": getattr(attacker, "attack_range", 1)
            }
        )
    """
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
                            "healed": agentDamage,
                            "healing_range": agentRange
                        }
                    )
                else:
                    log_event(
                        "character_attack",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id,
                            "attacker_id": agentLabel,
                            "target_id": target,
                            "damage": agentDamage,
                            "attack_range": agentRange
                        }
                    )
            else:
                log_event(
                    "enemy_attack",
                    level_id,
                    stage_id,
                    session_id,
                    user_id,
                    {   "session_id":session_id,
                        "enemy_id": agentLabel,
                        "target_id": target,
                        "damage": agentDamage
                    }
                )
    """
    def enemy_attack():
        global total_damage_taken
        if len(enemies) == 0 or len(players) == 0:
            return
        enemy = enemies[0]
        target = players[0]
        damage = 5
        # damage_agent(target, damage)
        total_damage_taken += damage
        
        log_event(
            "enemy_attack",
            level_id,
            stage_id,
            {   "session_id":session_id,
                "enemy_id": getattr(enemy, "name", "enemy_0"),
                "target_id": getattr(target, "name", "player_0"),
                "damage": damage
            }
        )
    """
    #Time
    clock = pygame.time.Clock()
    dt = 0
    frame = 0
    frameModifier = 0.125
    actualFrame = 0
    moveFrame = 0
    damageFrame = 0
    framesPerDamage=params["gameplay"]["frames_per_damage"]
    #framesPerDamage = 16
    animating = False
    animatingMove = False
    movementDone = False
    damageLogged = False
    #game loop
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
                        {   "session_id":session_id,
                            "turn_number": turn_number
                        }
                    )
                    log_event(
                        "stage_fail",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id,
                            "turns_taken": turn_number,
                            "failure_reason": "window_closed"
                        }
                    )
                    log_event(
                        "session_end",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id,
                            "stages_completed": (3*level_id + stage_id)
                        }
                    )
                running = False
            if event.type == pygame.WINDOWSIZECHANGED:
                screenWidth = screen.get_width()
                screenHeight = screen.get_height()
                size = findSize(screen, rows, cols)
                updateSize = True
            if event.type == pygame.MOUSEBUTTONUP:
                if active_side == "player" and not(animating):
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
                        if not(playerClicked):
                            player = players[playerI]
                            playerPos, _ = player.getPositions()
                            if playerPos.x == clickedCol and playerPos.y == clickedRow and activePlayer != playerI and player.findAlive() == 1:
                                playerClicked = True
                                activePlayer = playerI
                                # print(playerI)
                    # If clicking a player, then the active player is changed, so do not move the position
                    if playerClicked:
                        continue
                    moveSuccessful = players[activePlayer].attemptToMove(clickedRow, clickedCol, players)
                    """ no: movement occurs at the end of a player turn, NOT when a position is clicked.
                    if moveSuccessful:
                        log_event("character_move",
                                level_id,
                                stage_id,
                                {"session_id":session_id,
                                "character_id": players[activePlayer].getLabel(),
                                "to_row": clickedRow,
                                "to_col": clickedCol,
                                "turn_number":turn_number
                                }
                                )
                    """
                    # Only update the open spaces if the move was succesful
                    if moveSuccessful:
                        for player in players:
                            player.getMoveableLocations(cols, rows, obstacles, players, enemies, False)
                        for enemy in enemies:
                            enemy.getMoveableLocations(cols, rows, obstacles, players, enemies)
            #TEMP: fullscreen adjustment
            if event.type == pygame.KEYUP:
                
                # debugger: press W to force win (sets all enemies HP to 0)
                if event.key == pygame.K_w and stage_running:
                    for enemy in enemies:
                        enemy.setHP(0)
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
                #advance turn by pressing SPACEBAR - will log turn advance after animation
                if event.key == pygame.K_SPACE and stage_running:
                    # print("space works") quantum glitch : didnt work, added this(changed nothing else), it started working (my code works.... why??????????)
                    animating = True
                    animatingMove = True
                    if active_side == "player":
                        for player in players:
                            player.getMoveableLocations(cols, rows, obstacles, players, enemies, False)
                            player.getMovementPath()
                            moveFrame = 0
                            """
                    log_event(
                        "turn_end", 
                        level_id,
                        stage_id,
                        {
                            "session_id":session_id,
                            "turn_number":turn_number,
                            "active_side": active_side
                        }
                    )
                    advance_turn()
                    log_event(
                        "turn_start",
                        level_id,
                        stage_id,
                        {   "session_id":session_id,
                            "turn_number": turn_number,
                            "active_side": active_side
                        }
                    )
                    """
                #quit mid-stage by pressing ESC
                if event.key == pygame.K_ESCAPE and stage_running:
                    stage_running = False
                    log_event(
                        "quit",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id,
                            "turn_number": turn_number
                        }
                    )
                    log_event(
                        "stage_fail",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id,
                            "turns_taken": turn_number,
                            "failure_reason": "quit"
                        }
                    )
                    log_event(
                        "session_end",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id,
                            "stages_completed": (3*level_id + stage_id)
                        }
                    )
                    running = False
                """
                Attacks run automatically
                #player attacks (press A), only on player turn
                if event.key == pygame.K_a and stage_running and active_side == "player":
                    player_attack()
                
                #enemy attacks (press E), only on enemy turn
                if event.key == pygame.K_e and stage_running and active_side == "enemy":
                    enemy_attack()
                """
        if animating:
            animatingAgents = players if active_side == "player" else enemies
            # Animate Movement
            if animatingMove:
                """
                for agent in animatingAgents:
                    agent.moveAlongPath()
                """
                if all([agent.getMovesLeft() == 0 for agent in animatingAgents]):
                    movementDone = True
                if movementDone:
                    for agent in animatingAgents:
                        agent.updatePosition(agent.getMoveTo())
                    # Update the moveable locations for both players and enemies
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
                            # DELETE IF HP IS 0
                            if enemy.findAlive() == 1:
                                enemiesAfterTurn.append(enemy)
                            # else log enemy defeated?
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
                                "session_id":session_id,
                                "turn_number":turn_number,
                                "active_side": active_side
                                }
                            )
                        active_side, turn_number = advance_turn(active_side, turn_number)
                        log_event(
                            "turn_start",
                            level_id,
                            stage_id,
                            session_id,
                            user_id,
                            {   "session_id":session_id,
                                "turn_number": turn_number,
                                "active_side": active_side
                            }
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
                            # This can be used for both medic and enemies, since it will cause medic to heal the other players
                            else:
                                targets = agent.attack(players)
                                logAttack(agent, agent.getLabel() == "medic", targets)
                    damageFrame = 0
                    damageLogged = True
        #stage-end conditions (succeed/fail) - Moved this up, better to deal with this before rendering, as it's technically part of the gameplay 🙂
        if stage_running:
            if stage_won(enemies):
                
                log_event(
                    "stage_complete",
                    level_id,
                    stage_id,
                    session_id,
                    user_id,
                    {   "session_id":session_id,
                        "turns_taken": turn_number,
                        "characters_alive": sum(p.findAlive() for p in players),
                        "total_damage_taken": total_damage_taken
                    }
                )
                stage_id+=1
                if stage_id == 3:

                    log_event( # you might want to change payload - level stuff added by James, didnt do rest of telemetry
                        "level_complete",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id,
                            # dont think this can be done again here, as its for stages - "turns_taken": turn_number,
                            "characters_alive": sum(p.findAlive() for p in players),
                            # dont think this can be done again here, as its for stages - "total_damage_taken": total_damage_taken
                        }
                    ) 
                    """
                    move to level selector, just commenting this out for now
                    log_event(
                        "session_end",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id,
                            "stages_completed": (3*level_id + stage_id)
                        }
                    )
                    """
                    running = False
                    levelCompleted = True

                    """#file exists, -> load Stage 0 for next Level
                    level_id+=1
                    stage_id=0

                    #duplicate code might want to make a function
                    playerPlaces = [[brawlerRow, brawlerCol], [bomberRow, bomberCol], [medicRow, medicCol]]
                    size = findSize(screen, rows, cols)
                    top = (screenHeight - (size * rows)) // 2
                    left = (screenWidth - (size * cols)) // 2
                    tiles = [[c.TILE(size, row, col, left + (col * size), top + (row * size), "tile") for col in range(cols)] for row in range(rows)]
                    obstacles = [c.OBSTACLE(pygame.math.Vector2(obstacle[1], obstacle[0]), "obstacle") for obstacle in obstaclePlaces]
                    # Get player and enemy information
                    playerInfo, enemyInfo = getPlayerAndEnemyInformation(difficultyModifier)
                    # Temporary: Assign each player a set position, PLAYER COPYING IS NEEDED STILL
                    players = []
                    rowPlace = 0
                    for player in playerInfo:
                        playerForLevel = player.copySelf()
                        playerForLevel.updatePosition(pygame.math.Vector2(playerPlaces[rowPlace][1], playerPlaces[rowPlace][0]))
                        players.append(playerForLevel)
                        rowPlace += 1

                    loadStage(stage_id, stages, enemyInfo)

                    log_event( # you might want to change payload - level stuff added by James, didnt do rest of telemetry
                        "level_start",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id, 
                            #dont think this can be done again here, as its for stages - "enemy_count": len(enemies),
                            "grid_size": f"{rows}x{cols}"
                        }
                    )

                    log_event(
                        "stage_start",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id, 
                            "enemy_count": len(enemies),
                            "grid_size": f"{rows}x{cols}"
                        }
                    )"""
                    
                else:            
                    enemies = loadStage(stage_id, stages, enemyInfo)

                    log_event(
                        "stage_start",
                        level_id,
                        stage_id,
                        session_id,
                        user_id,
                        {   "session_id":session_id, 
                            "enemy_count": len(enemies),
                            "grid_size": f"{rows}x{cols}"
                        }
                    )
                    active_side = "player"
                    turn_number = 1 # reset may not be needed?
                    activePlayer = getActiveFromAlive(players, activePlayer)
                    for player in players:
                        player.startTurn(cols, rows, obstacles, players, enemies)
                    animating = False
                    animatingMove = False


                # running = False
        
            elif stage_lost(players):
                stage_running = False
                log_event(
                    "stage_fail",
                    level_id,
                    stage_id,
                    session_id,
                    user_id,
                    {   "session_id":session_id,
                        "turns_taken": turn_number,
                        "failure_reason": "all_players_defeated"
                    }
                )
                log_event(
                    "session_end",
                    level_id,
                    stage_id,
                    session_id,
                    user_id,
                    {   "session_id":session_id,
                        "stages_completed": (3*level_id + stage_id)
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
        for playerI, player in enumerate(players):
            showRender = player.findAlive() == 1 or not(doHide)
            player.render(screen, tiles, actualFrame, moveFrame, showRender, active_side == "player" and not(animating) and player.findAlive() == 1, True, activePlayer == playerI)
        # Render enemy agents
        for enemy in enemies:
            enemy.render(screen, tiles, actualFrame, moveFrame, True)
        # Render obstacles
        for obstacle in obstacles:
            obstacle.render(screen, tiles)
        # HP Rendered after everything else rendered, to allow it to be shown on top of everything else
        # Render HP of all player agents
        for player in players:
            showRender = player.findAlive() == 1
            player.renderHP(screen, tiles, moveFrame, damageFrame, showRender)
        # Render HP of all enemy agents
        for enemy in enemies:
            enemy.renderHP(screen, tiles, moveFrame, damageFrame, True)
        pygame.display.flip()
        # Update time and frame
        fps=params["gameplay"]["fps"]
        dt=clock.tick(fps)
        #dt = clock.tick(30)
        frame = frame + frameModifier
        actualFrame = m.floor(frame)
        moveFrame += 1
    return levelCompleted
# pygame.quit()
if __name__ == '__main__':
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
    for levelNum in range(2):
        playLevel(levelNum, 0, screen, fullscreen, oldWidth, oldHeight, monitorWidth, monitorHeight)
