import pygame
import math as m
# Tile Class: Stores size, row, column, x, y and picture
class TILE:
    def __init__(self, size, row, col, x, y, imgLocation):
        self.size = size
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        try:
            self.img = pygame.image.load(f"assets/{imgLocation}.png")
        except:
            # Use the default texture not found texture
            self.img = pygame.Surface((32, 32))
            pygame.draw.rect(self.img, pygame.Color(255, 0, 255), (0, 0, 16, 16))
            pygame.draw.rect(self.img, pygame.Color(255, 0, 255), (16, 16, 16, 16))
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
    def getSize(self):
        return self.size
    # Get whether the mouse clicked this tile, and return row/col if so (if not, return -1, -1)
    def getClicked(self, mx, my):
        if (self.x <= mx and mx <= self.x + self.size) and (self.y <= my <= self.y + self.size):
            return self.row, self.col
        return -1, -1
class OBSTACLE:
    def __init__(self, pos, imgLocation):
        self.pos = pos
        try:
            self.img = pygame.image.load(f"assets/{imgLocation}.png")
        except:
            # Use the default texture not found texture
            self.img = pygame.Surface((32, 32))
            pygame.draw.rect(self.img, pygame.Color(255, 0, 255), (0, 0, 16, 16))
            pygame.draw.rect(self.img, pygame.Color(255, 0, 255), (16, 16, 16, 16))
    # Get the position and size of the tile, depending on its position and tile size
    def getRenderPosAndSize(self, tiles):
        tile = tiles[round(self.pos.y)][round(self.pos.x)]
        xRender, yRender = tile.getPosition()
        sizeRender = tile.getSize()
        return xRender, yRender, sizeRender
    # Render the obstacle
    def render(self, screen, tiles):
        xRender, yRender, sizeRender = self.getRenderPosAndSize(tiles)
        # Scale and render the sprite
        spriteScaled = pygame.transform.scale(self.img, (sizeRender, sizeRender))
        screen.blit(spriteScaled, (xRender, yRender))
    def getPosition(self):
        return self.pos
# Parent Class: Agent, used as a base for both the player and enemy class
class AGENT:
    def __init__ (self, maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName, label):
        self.maxHP = maxHP
        self.HP = maxHP
        self.prevHP = maxHP
        self.baseAtk = baseAtk
        self.atk = baseAtk
        self.atkRange = atkRange
        self.moveSpeed = moveSpeed
        # Pos is given as a vect2, where the x corresponds to the column, and the y corresponds to the row
        self.pos = pos.copy()
        self.resetMoveToPos()
        self.previousPosition = self.pos.copy()
        self.spritesheetName = spritesheetName
        try:
            self.spritesheet = pygame.image.load(f"assets/{spritesheetName}.png")
        except:
            # Use the default texture not found texture
            self.spritesheet = pygame.Surface((32, 32))
            pygame.draw.rect(self.spritesheet, pygame.Color(255, 0, 255), (0, 0, 16, 16))
            pygame.draw.rect(self.spritesheet, pygame.Color(255, 0, 255), (16, 16, 16, 16))
        try:
            self.hpBar = pygame.image.load("assets/HPBar.png")
        except:
            self.hpBar = None
        self.faceRight = False
        try:
            self.activeBox = pygame.image.load("assets/ActiveOutline.png")
        except:
            self.activeBox = None
        self.label = label
        self.movementPath = [] # default to blank to avoid issues
        self.framesPerTile = 8
        self.framesForDamage = 16
        self.attackMod = 1
    def getBaseFacingDir(self, stageWidth):
        self.faceRight = self.pos.x < stageWidth // 2
    # Returns true if the label is the same as own label, else returns false
    def checkLabel(self, label):
        return label == self.label
    def getLabel(self):
        return self.label
    def getAttack(self):
        return round(self.atk * self.attackMod)
    def getAttackRange(self):
        return self.atkRange
    # Create a copy of the agent, keeping its class
    def copySelf(self):
        return type(self)(self.maxHP, self.baseAtk, self.atkRange, self.moveSpeed, self.pos, self.spritesheetName, self.label)
    # Get the position and size of the agent, depending on its position and tile size
    def getRenderPosAndSize(self, tiles, moveFrame, fromMainRender = False):
        tile = tiles[round(self.pos.y)][round(self.pos.x)]
        if moveFrame % self.framesPerTile == 0 and fromMainRender:
            self.moveAlongPath()
        if len(self.movementPath) == 0:
            xRender, yRender = tile.getPosition()
            yDir = 0
        else:
            tilePrev = tiles[round(self.previousPosition.y)][round(self.previousPosition.x)]
            prevTileX, prevTileY = tilePrev.getPosition()
            newTileX, newTileY = tile.getPosition()
            diffAmount = (moveFrame % self.framesPerTile) / self.framesPerTile
            xRender = round(pygame.math.lerp(prevTileX, newTileX, diffAmount))
            yRender = round(pygame.math.lerp(prevTileY, newTileY, diffAmount))
            # yDir : way the character faces in the y direction, only used for movement animation
            yDir = 0
            if prevTileY > newTileY:
                # Going up
                yDir = -1
            elif prevTileY < newTileY:
                # Going down
                yDir = 1
            # faceRight: Stored, used for full rendering (character faces last direction they moved)
            self.faceRight = newTileX >= prevTileX
            # xRender, yRender = tile.getPosition()
        sizeRender = tile.getSize()
        return xRender, yRender, sizeRender, yDir
    def getMoveToRenderPos(self, tiles):
        tile = tiles[round(self.moveTo.y)][round(self.moveTo.x)]
        xRender, yRender = tile.getPosition()
        return xRender, yRender
    # Scan for first possible tile to move from, following order up, down, left, right
    def scanForTile(self, lookingFor, position):
        posRow, posCol = round(position.y), round(position.x)
        for i in range(4):
            # Deals with y change
            rowChange = 2 * i - 1 if i // 2 == 0 else 0
            # Deals with x change
            colChange = 2 * i - 5 if i // 2 == 1 else 0
            scanRow, scanCol = posRow + rowChange, posCol + colChange
            rowFits = scanRow >= 0 and scanRow < len(self.moveableLocations)
            colFits = scanCol >= 0 and scanCol < len(self.moveableLocations[0])
            if rowFits and colFits and self.moveableLocations[scanRow][scanCol] == lookingFor:
                return pygame.Vector2((scanCol, scanRow))
        # This shouldn't occur, but for safety, return agent base position
        playerPosCopy = self.pos.copy()
        return playerPosCopy
    # Find the path the agent should move on
    def findPath(self, lookingFor, position):
        # If looking for minus one, then this is the tile the agent is on
        if lookingFor == -1:
            playerPosCopy = self.pos.copy()
            return [playerPosCopy]
        previousPosition = self.scanForTile(lookingFor, position)
        previousTiles = self.findPath(lookingFor - 1, previousPosition)
        previousTiles.append(position.copy())
        return previousTiles
    def getMovementPath(self):
        moveToAmount = self.moveableLocations[round(self.moveTo.y)][round(self.moveTo.x)]
        self.movementPath = self.findPath(moveToAmount - 1, self.moveTo)
    # Move along path
    def moveAlongPath(self):
        if len(self.movementPath) > 0:
            self.previousPosition = self.movementPath[0].copy()
            self.movementPath.pop(0)
            if len(self.movementPath) > 0:
                self.pos = self.movementPath[0].copy()
            else:
                self.pos = self.moveTo.copy()
    # Get number of moves left
    def getMovesLeft(self):
        return len(self.movementPath)
    # Render the agent
    def render(self, screen, tiles, frame, moveFrame, show, selectingPosition = False, player = False, activePlayer = False):
        xRender, yRender, sizeRender, yDir = self.getRenderPosAndSize(tiles, moveFrame, True)
        animFrame = frame % 4
        # Medic has animation (supports any with name eventually)
        if self.spritesheetName in ["medic", "brawler", "bomber", "en0", "en1"]:
            spritesheetCol = animFrame
            """
            ROWS:
            0: idle forwards, not used in game
            1: idle side, used for everything except walking
            2: walk side
            3: walk forwards
            4: walk backwards
            5: Defeated
            """
            # If ydir is not 0, then moving up or down
            if self.HP == 0 and self.HP == self.prevHP and player:
                spritesheetRow = 5
            elif yDir == -1:
                spritesheetRow = 4
            elif yDir == 1:
                spritesheetRow = 3
            elif len(self.movementPath) != 0:
                spritesheetRow = 2
            else:
                spritesheetRow = 1
        # Others do not, so use a single sprite (found at row 0, column 0 in sprite sheet)
        else:
            spritesheetRow = 0
            spritesheetCol = 0
        # Only get the current sprite. SRCALPHA flag ensures a transparent background
        if show:
            sprite = pygame.Surface((32, 32), flags = pygame.SRCALPHA)
            sprite.blit(self.spritesheet, (0, 0), (spritesheetCol * 32, spritesheetRow * 32, 32, 32))
            # Scale, flip (if necessary) and render the sprite
            spriteScaled = pygame.transform.flip(pygame.transform.scale(sprite, (sizeRender, sizeRender)), self.faceRight, False)
            screen.blit(spriteScaled, (xRender, yRender))
        if player and selectingPosition:
            # Render position being moved to, if this is different to the current position
            if not(self.moveTo.distance_to(self.pos) == 0):
                moveToX, moveToY = self.getMoveToRenderPos(tiles)
                if show:
                    spriteAlpha = spriteScaled.copy()
                    spriteAlpha.set_alpha(128)
                    screen.blit(spriteAlpha, (moveToX, moveToY))
            # Render if the tile is active and the active outline was successfully loaded
            if self.activeBox != None and show:
                if activePlayer:
                    # Draw a 5x5 rectangle, 1 pixel away from top of sprite
                    activeX, activeY = xRender + sizeRender // 32, yRender + sizeRender // 32
                    activeSize = 5 * sizeRender // 32
                    pygame.draw.rect(screen, "green", (activeX, activeY, activeSize, activeSize))
                activeScaled = pygame.transform.scale(self.activeBox, (sizeRender, sizeRender))
                screen.blit(activeScaled, (xRender, yRender))

    # Render the HP bar of the agent
    def renderHP(self, screen, tiles, moveFrame, damageFrame, show):
        # Only run if the HP bar was successfully loaded and the sprite is being shown
        if self.hpBar == None or not(show):
            return
        xRender, yRender, sizeRender, _ = self.getRenderPosAndSize(tiles, moveFrame)
        if self.HP == self.prevHP:
            hpPercentage = self.HP / self.maxHP
        else:
            hpPercentage = pygame.math.lerp(self.prevHP / self.maxHP, self.HP / self.maxHP, damageFrame / self.framesForDamage)
        hpColor = 2 * hpPercentage
        if hpColor > 1:
            hpColor -= 1
            hpBarColor = pygame.Color(255, 255, 0).lerp(pygame.Color(0,255,0), hpColor)
        else:
            hpBarColor = pygame.Color(255, 0, 0).lerp(pygame.Color(255,255,0), hpColor)
        # Base pixels for the rectangle
        hpBarBaseWidth = 28
        hpBarBaseHeight = 4
        hpBarBaseTop = 26
        hpBarBaseLeft = 2
        hpImgOffset = m.ceil(12 * sizeRender / 32)
        hpRectTop = m.ceil(hpBarBaseTop * sizeRender / 32) + yRender
        hpRectLeft = m.ceil(hpBarBaseLeft * sizeRender / 32) + xRender
        hpRectWidth = m.ceil(hpBarBaseWidth * sizeRender * hpPercentage / 32)
        hpRectHeight = m.ceil(hpBarBaseHeight * sizeRender / 32)
        pygame.draw.rect(screen, hpBarColor, (hpRectLeft, hpRectTop, hpRectWidth, hpRectHeight))
        hpScaled = pygame.transform.scale(self.hpBar, (sizeRender, sizeRender))
        screen.blit(hpScaled, (xRender, yRender + hpImgOffset))
    # Reset the move to position at the start of each turn, and upon load
    def resetMoveToPos(self):
        self.moveTo = self.pos.copy()
    # Get position to move to - for testing, will eventually have animation
    def getMoveTo(self):
        return self.moveTo
    # Reset the position of the agent
    def updatePosition(self, pos):
        self.pos.update(pos.copy())
        self.moveTo.update(pos.copy())
    # Flood Fill: Used for finding all possible spaces an agent can move to
    def floodFill(self, searchFor, flooded, env):
        if self.moveSpeed == searchFor:
            return flooded
        fillFor = searchFor + 1
        changed = False
        for rowI in range(len(flooded)):
            row = flooded[rowI]
            for colI in range(len(row)):
                col = row[colI]
                if col == searchFor:
                    # Scan above, left, right, down
                    for scanChange in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                        rowChange, colChange = rowI + scanChange[0], colI + scanChange[1]
                        # check whether in range
                        if 0 <= rowChange and rowChange < len(flooded) and 0<= colChange and colChange < len(row):
                            # Check that the area is not flooded already, and that it can be moved to
                            if env[rowChange][colChange] and flooded[rowChange][colChange] == -1:
                                flooded[rowChange][colChange] = fillFor
                                changed = True
        # Only continue recursion if there has been a change, reduce risk of stack overflow
        if changed:
            return self.floodFill(fillFor, flooded, env)
        return flooded
    # Find all open tiles
    def getOpenTiles(self, gridWidth, gridHeight, obstacles, playerAgents, enemyAgents, considerMoveTo = True):
        baseArea = [[-1 for col in range(gridWidth)] for row in range(gridHeight)]
        baseArea[round(self.pos.y)][round(self.pos.x)] = 0
        env = [[True for col in range(gridWidth)] for row in range(gridHeight)]
        for obstacle in obstacles:
            obstaclePos = obstacle.getPosition()
            obstacleRow, obstacleCol = obstaclePos.y, obstaclePos.x
            env[round(obstacleRow)][round(obstacleCol)] = False
        # Update the environment for player agents, to prevent overlaps
        for player in playerAgents:
            playerPos, playerMoveToPos = player.getPositions()
            # Only update env if the start and end positions to not match own start and end positions
            if self.pos.distance_to(playerPos) == 0 and self.moveTo.distance_to(playerMoveToPos) == 0:
                continue
            env[round(playerPos.y)][round(playerPos.x)] = False
            if considerMoveTo:
                env[round(playerMoveToPos.y)][round(playerMoveToPos.x)] = False
        # Update the environment for enemy agents, to prevent overlaps
        for enemy in enemyAgents:
            enemyPos, enemyMoveToPos = enemy.getPositions()
            # Only update env if the start and end positions to not match own start and end positions
            if self.pos.distance_to(enemyPos) == 0 and self.moveTo.distance_to(enemyMoveToPos) == 0:
                continue
            env[round(enemyPos.y)][round(enemyPos.x)] = False
            if considerMoveTo:
                env[round(enemyMoveToPos.y)][round(enemyMoveToPos.x)] = False
        return baseArea, env
    # Find all moveable locations, given the size of the grid, an array of all players, and an array of all enemies
    def getMoveableLocations(self, gridWidth, gridHeight, obstacles, playerAgents, enemyAgents, considerMoveTo = True):
        baseArea, env = self.getOpenTiles(gridWidth, gridHeight, obstacles, playerAgents, enemyAgents, considerMoveTo)
        self.moveableLocations = self.floodFill(0, baseArea, env)
    # Returns the current and move to positions
    def getPositions(self):
        return self.pos, self.moveTo
    # Attack all agents within range
    def attack(self, agents):
        attackedAgents  = []
        for agent in agents:
            agentPos, _ = agent.getPositions()
            if self.pos.distance_to(agentPos) <= self.atkRange:
                attackedAgents.append(agent.getLabel())
                agent.loseHP(round(self.atk * self.attackMod))
        return attackedAgents
    def loseHP(self, amount):
        # Always sets the HP to 0 as a minumum, and maxHP as a maximum
        self.HP = min(self.maxHP, max(0, self.HP - amount))
    def setHP(self, amount):
        self.HP = amount
    # Return 1 if the agent is alive, else 0. Use previous to allow for animation
    def findAlive(self):
        return 1 if self.prevHP > 0 else 0
    def getLabel(self):
        return self.label
    def setLabel(self, label):
        self.label = label
    def matchCurrToPrevHP(self):
        self.prevHP = self.HP
# Enemy Class: Class representing an enemy.
class ENEMY(AGENT):
    def __init__ (self, maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName, label, attackMod = 1):
        super().__init__(maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName, label)
        self.attackMod = attackMod
    def copySelf(self):
        return type(self)(self.maxHP, self.baseAtk, self.atkRange, self.moveSpeed, self.pos, self.spritesheetName, self.label, self.attackMod)
    def findOptimalMoveLocation(self, gridWidth, gridHeight, obstacles, playerAgents, enemyAgents):
        self.getMoveableLocations(gridWidth, gridHeight, obstacles, playerAgents, enemyAgents)
        playerPositions = []
        for player in playerAgents:
            if player.findAlive() == 1:
                playerPos, _ = player.getPositions()
                playerPositions.append(playerPos)
        # Only run if all the players are alive
        if len(playerPositions) == 0:
            self.moveTo.update(self.pos)
            return
        # First find area within movement range with the maximum players within range
        maxInRange = 0
        maxPos = pygame.math.Vector2((0,0))
        closestDist = -1
        closestPos = pygame.math.Vector2((0,0))
        for rowI in range(len(self.moveableLocations)):
            for colI in range(len(self.moveableLocations[rowI])):
                if self.moveableLocations[rowI][colI] != -1:
                    testPos = pygame.math.Vector2((colI, rowI))
                    testInRange = 0
                    testDist = 0
                    for playerPosition in playerPositions:
                        distToPlayer = testPos.distance_to(playerPosition)
                        testDist += distToPlayer
                        if distToPlayer <= self.atkRange:
                            testInRange += 1
                    if testInRange > maxInRange or (testInRange == maxInRange and testPos.distance_to(self.pos) < maxPos.distance_to(self.pos)):
                        maxInRange = testInRange
                        maxPos.update(testPos.copy())
                    testDist /= len(playerPositions)
                    if testDist < closestDist or closestDist == -1:
                        closestDist = testDist
                        closestPos.update(testPos.copy())
        if maxInRange > 0:
            self.moveTo.update(maxPos)
            return
        # If there are no targets in range, move towards the closest target. TEMP: Base this on average distance to players, no pathfinding
        self.moveTo.update(closestPos)
    def spawnFixScan(self, lookingFor, possibleLocations, openLocations):
        rowI = 0
        for row in possibleLocations:
            colI = 0
            for col in row:
                if col == lookingFor:
                    # Scan above, left, right, down
                    for scanChange in [[-1, 0], [0, -1], [0, 1], [1, 0]]:
                        rowChange, colChange = rowI + scanChange[0], colI + scanChange[1]
                        # check whether in range
                        if 0 <= rowChange and rowChange < len(possibleLocations) and 0<= colChange and colChange < len(row):
                            # Check that the area is open, and move there
                            if openLocations[rowChange][colChange] and possibleLocations[rowChange][colChange] == -1:
                                return pygame.Vector2((colChange, rowChange))
                            possibleLocations[rowChange][colChange] = lookingFor + 1
                colI += 1
            rowI += 1
        return self.spawnFixScan(lookingFor + 1, possibleLocations, openLocations)
    def fixSpawn(self, gridWidth, gridHeight, obstacles, playerAgents, enemyAgents):
        # Scan around, find nearest that is not occupied by a player, obstacle or enemy
        openLocations = [[True for col in range(gridWidth)] for row in range(gridHeight)]
        for obstacle in obstacles:
            obstaclePos = obstacle.getPosition()
            obstacleRow, obstacleCol = obstaclePos.y, obstaclePos.x
            openLocations[round(obstacleRow)][round(obstacleCol)] = False
        # Update the environment for player agents, to prevent overlaps
        for player in playerAgents:
            playerPos, _ = player.getPositions()
            openLocations[round(playerPos.y)][round(playerPos.x)] = False
        # Update the environment for enemy agents, to prevent overlaps
        for enemy in enemyAgents:
            enemyPos, _ = enemy.getPositions()
            # Only update env if the start and end positions to not match own start and end positions
            if enemy.getLabel() == self.label:
                continue
            openLocations[round(enemyPos.y)][round(enemyPos.x)] = False
        if openLocations[round(self.pos.y)][round(self.pos.x)]:
            return
        possibleLocations = [[-1 for col in range(gridWidth)] for row in range(gridHeight)]
        possibleLocations[round(self.pos.y)][round(self.pos.x)] = 0
        self.pos.update(self.spawnFixScan(0, possibleLocations, openLocations).copy())
# Player Class: Class representing a player character. NOTE: Medic does NOT use this class, instead uses a child class of player
class PLAYER(AGENT):
    def __init__ (self, maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName, label):
        super().__init__(maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName, label)
        self.playerTurn = False
    # Start turn by finding all possible locations to move to
    def startTurn(self, gridWidth, gridHeight, obstacles, playerAgents, enemyAgents):
        self.getMoveableLocations(gridWidth, gridHeight, obstacles, playerAgents, enemyAgents, False)
        self.playerTurn = True
    # End turn
    def endTurn(self):
        self.playerTurn = False
    # Attempt to move to where mouse clicked (Calculated ourside of class), returns if this is successful, as the moveable locations will need to be updated following this
    def attemptToMove(self, mouseRow, mouseCol, players):
        if self.playerTurn:
            taken = False
            for player in players:
                # If the labels are the same, this is the player
                if player.getLabel() == self.label:
                    continue
                _, playerCheckPos = player.getPositions()
                if playerCheckPos.x == mouseCol and playerCheckPos.y == mouseRow:
                    taken = True
            if self.moveableLocations[mouseRow][mouseCol] != -1 and not(taken):
                self.moveTo.update(mouseCol, mouseRow)
                return True
        return False
    # Set move to location to where the player clicked IF POSSIBLE
# Medic Class: Subclass of Player, to override attack to be a heal
class MEDIC(PLAYER):
    def __init__ (self, maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName, label):
        super().__init__(maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName, label)
    def attack(self, players):
        healedPlayers = []
        for player in players:
            playerPos, _ = player.getPositions()
            distToPlayer = self.pos.distance_to(playerPos)
            if distToPlayer <= self.atkRange and distToPlayer != 0 and player.findAlive() == 1: # If distance is 0, then this is the healer, so can skip
                healedPlayers.append(player.getLabel())
                player.loseHP(-1 * self.atk) # Multiply by -1 meaning that the player will GAIN hp
        return healedPlayers