import pygame

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
        if (self.left <= mx and mx <= self.x + self.size) and (self.top <= my <= self.top + self.size):
            return self.row, self.col
        return -1, -1
# Parent Class: Agent, used as a base for both the player and enemy class
class AGENT:
    def __init__ (self, maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName):
        self.maxHP = maxHP
        self.HP = maxHP
        self.baseAtk = baseAtk
        self.atk = baseAtk
        self.atkRange = atkRange
        self.moveSpeed = moveSpeed
        # Pos is given as a vect2, where the x corresponds to the column, and the y corresponds to the row
        self.pos = pos
        self.resetMoveToPos()
        try:
            self.spritesheet = pygame.image.load(f"assets/{spritesheetName}.png")
        except:
            # Use the default texture not found texture
            self.spritesheet = pygame.Surface((32, 32))
            pygame.draw.rect(self.spritesheet, pygame.Color(255, 0, 255), (0, 0, 16, 16))
            pygame.draw.rect(self.spritesheet, pygame.Color(255, 0, 255), (16, 16, 16, 16))
    def render(self, screen, tiles):
        tile = tiles[round(self.pos.y)][round(self.pos.x)]
        xRender, yRender = tile.getPosition()
        sizeRender = tile.getSize()
        # For now, use a single sprite (found at row 0, column 0 in sprite sheet)
        spritesheetRow = 0
        spritesheetCol = 0
        # Only get the current sprite. SRCALPHA flag ensures a transparent background
        sprite = pygame.Surface((32, 32), flags = pygame.SRCALPHA)
        sprite.blit(self.spritesheet, (0, 0), (spritesheetCol * 32, spritesheetRow * 32, 32, 32))
        # Scale and render the sprite
        spriteScaled = pygame.transform.scale(sprite, (sizeRender, sizeRender))
        screen.blit(spriteScaled, (xRender, yRender))
    # Reset the move to position at the start of each turn, and upon load
    def resetMoveToPos(self):
        self.moveTo = self.pos
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
                        if 0 <= rowChange and rowChange < len(flooded) and 0<= colChange and colChange < len(col):
                            # Check that the area is not flooded already, and that it can be moved to
                            if env[rowChange][colChange] and flooded[rowChange][colChange] == -1:
                                flooded[rowChange][colChange] = fillFor
                                changed = True
        # Only continue recursion if there has been a change, reduce risk of stack overflow
        if changed:
            return self.floodFill(fillFor, flooded, env)
        return flooded
    # Find all open tiles
    def getOpenTiles(self, gridWidth, gridHeight, obstacles, playerAgents, enemyAgents):
        baseArea = [[-1 for col in gridWidth] for row in gridHeight]
        baseArea[round(self.pos.y)][round(self.pos.x)] = 0
        env = [[True for col in gridWidth] for row in gridHeight]
        """
        for obstacle in obstacles:
            obstaclePos = obstacle.getPosition()
            obstacleRow, obstacleCol = obstaclePos.y, obstaclePos.x
            env[obstacleRow][obstacleCol] = False
        """
        # Update the environment for player agents, to prevent overlaps
        for player in playerAgents:
            playerPos, playerMoveToPos = player.getPositions()
            # Only update env if the start and end positions to not match own start and end positions
            if self.pos.distance_to(playerPos) == 0 and self.moveTo.distance_to(playerMoveToPos) == 0:
                continue
            env[round(playerPos.y)][round(playerPos.x)] = False
            env[round(playerMoveToPos.y)][round(playerMoveToPos.x)] = False
        # Update the environment for enemy agents, to prevent overlaps
        for enemy in enemyAgents:
            enemyPos, enemyMoveToPos = enemy.getPositions()
            # Only update env if the start and end positions to not match own start and end positions
            if self.pos.distance_to(enemyPos) == 0 and self.moveTo.distance_to(enemyMoveToPos) == 0:
                continue
            env[round(enemyPos.y)][round(enemyPos.x)] = False
            env[round(enemyMoveToPos.y)][round(enemyMoveToPos.x)] = False
        return baseArea, env
    # Find all moveable locations, given the size of the grid, an array of all players, and an array of all enemies
    def getMoveableLocations(self, gridWidth, gridHeight, obstacles, playerAgents, enemyAgents):
        baseArea, env = self.getOpenTiles(gridWidth, gridHeight, obstacles, playerAgents, enemyAgents)
        self.moveableLocations = self.floodFill(0, baseArea, env)
    # Returns the current and move to positions
    def getPositions(self):
        return self.pos, self.moveTo
    # Attack all agents within range
    def attack(self, agents):
        for agent in agents:
            agentPos, _ = agent.getPositions()
            if self.pos.distance_to(agentPos) <= self.atkRange:
                agent.loseHP(self.atk)
    def loseHP(self, amount):
        # Always sets the HP to 0 as a minumum, and maxHP as a maximum
        self.HP = min(self.maxHP, max(0, self.HP - amount))
# Enemy Class: Class representing an enemy.
class ENEMY(AGENT):
    def __init__ (self, maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName):
        super().__init__(maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName)
    def findOptimalMoveLocation(self, gridWidth, gridHeight, obstacles, playerAgents, enemyAgents):
        self.getMoveableLocations(gridWidth, gridHeight, obstacles, playerAgents, enemyAgents)
        playerPositions = []
        for player in playerAgents:
            playerPos, _ = player.getPositions()
            playerPositions.append(playerPos)
        # First find area within movement range with the maximum players within range
        maxInRange = 0
        maxPos = pygame.math.Vector2((0,0))
        for rowI in range(len(self.moveableLocations)):
            for colI in range(len(self.moveableLocations[rowI])):
                testPos = pygame.math.Vector2((colI, rowI))
                testInRange = 0
                for playerPosition in playerPositions:
                    if testPos.distance_to(playerPosition) <= self.atkRange:
                        testInRange += 1
                if testInRange > maxInRange or (testInRange == maxInRange and testPos.distance_to(self.pos) < maxPos.distance_to(self.pos)):
                    maxInRange = testInRange
                    maxPos.update(testPos)
        if maxInRange > 0:
            self.moveTo.update(maxPos)
            return
        # If there are no targets in range, move towards the closest target.
        # TODO: WORK OUT HOW TO IMPLEMENT THIS
# Player Class: Class representing a player character. NOTE: Medic does NOT use this class, instead uses a child class of player
class PLAYER(AGENT):
    def __init__ (self, maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName):
        super().__init__(maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName)
        self.playerTurn = False
    # Start turn by finding all possible locations to move to
    def startTurn(self, env):
        self.getMoveableLocations(env)
        self.playerTurn = True
    # End turn
    def endTurn(self):
        self.playerTurn = False
    # Attempt to move to where mouse clicked (Calculated ourside of class), returns if this is successful, as the moveable locations will need to be updated following this
    def attemptToMove(self, mouseRow, mouseCol):
        if self.playerTurn:
            if self.moveableLocations[mouseRow, mouseCol] != -1:
                self.moveTo.update(mouseCol, mouseRow)
                return True
        return False
    # Set move to location to where the player clicked IF POSSIBLE
# Medic Class: Subclass of Player, to override attack to be a heal
class MEDIC(PLAYER):
    def __init__ (self, maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName):
        super().__init__(maxHP, baseAtk, atkRange, moveSpeed, pos, spritesheetName)
    def attack(self, players):
        for player in players:
            playerPos, _ = player.getPositions
            distToPlayer = self.pos.distance_to(playerPos)
            if distToPlayer <= self.atkRange and distToPlayer != 0: # If distance is 0, then this is the healer, so can skip
                player.loseHP(-1 * self.atk) # Multiply by -1 meaning that the player will GAIN hp