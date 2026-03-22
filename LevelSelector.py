import pygame
import mainGame
import pandas as pd

pygame.init()
def selectLevel(userID):
    class RecyclerView:
        def __init__(self, renderRect, itemWidth):
            self.renderRect = renderRect
            self.items = []
            self.index = 0
            self.t = float(1)
            self.fittableItems = renderRect.width // itemWidth + 2
            self.itemWidth = itemWidth
        # set the render rectangle
        def setRenderRect(self, renderRect):
            self.renderRect = renderRect
            self.fittableItems = renderRect.width // self.itemWidth + 2
        # set the width of the items
        def setItemWidth(self, itemWidth):
            self.itemWidth = itemWidth
            self.fittableItems = self.renderRect.width // itemWidth + 2
            for item in self.items:
                item.updateWidth(itemWidth)
        # populates the items
        def populate(self, items):
            for item in items:
                self.items.append(self.RecyclerViewItem(item, self.itemWidth))
        # adds an item at the given index, defaults to end of list
        def addItem(self, item, index = -1):
            if index == -1:
                self.items.append(self.RecyclerViewItem(item, self.itemWidth))
            else:
                self.items.insert(index, self.RecyclerViewItem(item, self.itemWidth))
        # removes an item at a given index, defaults to end of list
        def removeItem(self, index = -1):
            self.items.pop(index)
        # renders the RecyclerView
        def render(self, screen):
            renderSurface = pygame.Surface(self.renderRect.size, flags = pygame.SRCALPHA)
            for i in range(self.fittableItems):
                itemIndex = i + self.index
                if itemIndex < len(self.items):
                    self.items[itemIndex].render(renderSurface, self.t, i)
            screen.blit(renderSurface, self.renderRect)
        # sets the t: the scrolling
        def setT(self, t):
            self.t = t
        # changes the t: the scrolling
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
        # changes the index of the leftmost item
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
        # gets the index of the item clicked in the RecyclerView, or -1 if this is not found
        def getIndexClicked(self, mx, my):
            if self.renderRect.collidepoint(mx, my):
                for i in range(self.fittableItems):
                    itemIndex = i + self.index
                    if itemIndex < len(self.items):
                        if self.items[itemIndex].getClicked(mx, self.t, i):
                            return itemIndex
            return -1
        # for testing
        def getT(self):
            return self.t
        def getIndex(self):
            return self.index
        def updateDifficulties(self, playableDifficulties):
            for i, item in enumerate(self.items):
                item.updateDifficultiesCompleted({
                    'easyCompleted': playableDifficulties[0] > i,
                    'normalCompleted': playableDifficulties[1] > i,
                    'hardCompleted': playableDifficulties[2] > i})
        class RecyclerViewItem:
            def __init__(self, content, width):
                """
                content: dict, containing 5 values:
                font: font (just for rendering the level number). Will use upheaval font, as it's royalty free and pixel style to begin with
                levelNumber: int
                easyCompleted: bool
                normalCompleted: bool
                hardCompleted: bool
                """
                self.font = content['font']
                self.levelNumber = content['levelNumber']
                self.easyCompleted = content['easyCompleted']
                self.normalCompleted = content['normalCompleted']
                self.hardCompleted = content['hardCompleted']
                self.width = width
            def updateDifficultiesCompleted(self, content):
                self.easyCompleted = content['easyCompleted']
                self.normalCompleted = content['normalCompleted']
                self.hardCompleted = content['hardCompleted']
            def updateWidth(self, width):
                self.width = width
            def render(self, surface, t, indexFromStart):
                starPillow = 2
                surfaceWidth = self.width
                surfaceHeight = surface.get_height()
                baseSurface = pygame.Surface((surfaceWidth, surfaceHeight), flags = pygame.SRCALPHA)
                starSize = self.width // 3 - (2 * starPillow)
                textMaxHeight = surfaceHeight - starSize
                # Render level number, with black text and a white outline (render outline first).
                textOutlineWidth = 5
                textOutline = self.font.render(str(self.levelNumber), False, 'white')
                scale = min([(surfaceWidth - 2 * textOutlineWidth)/textOutline.get_width(), (textMaxHeight - 2 * textOutlineWidth)/textOutline.get_height()])
                textOutline = pygame.transform.scale_by(textOutline, scale)
                textMain = pygame.transform.scale_by(self.font.render(str(self.levelNumber), False, 'black'), scale)
                centerX = (surfaceWidth - textMain.get_width()) // 2
                centerY = (textMaxHeight - textMain.get_height()) // 2
                # Render outline
                for i in range(3):
                    for j in range(3):
                        baseSurface.blit(textOutline, (centerX + ((i - 1) * textOutlineWidth), centerY + ((j - 1) * textOutlineWidth)))
                # render main text
                baseSurface.blit(textMain, (centerX, centerY))
                # render stars
                starComplete = pygame.transform.scale(pygame.image.load("assets/difficultyComplete.png"), (starSize, starSize))
                starIncomplete = pygame.transform.scale(pygame.image.load("assets/difficultyIncomplete.png"), (starSize, starSize))
                starX = (surfaceWidth - 3 * (starSize + (2 * starPillow))) // 2
                for difficultyCompleted in [self.easyCompleted, self.normalCompleted, self.hardCompleted]:
                    if difficultyCompleted:
                        baseSurface.blit(starComplete, (starX, textMaxHeight))
                    else:
                        baseSurface.blit(starIncomplete, (starX, textMaxHeight))
                    starX += starSize + (2 * starPillow)
                # render item in recyclerview
                itemX = (t + indexFromStart - 1) * self.width
                surface.blit(baseSurface, (itemX, 0))
            def getClicked(self, mx, t, indexFromStart):
                minX = (t + indexFromStart - 1) * self.width
                maxX = minX + self.width
                return minX <= mx and mx <= maxX

    class Button:
        def __init__(self, baseRect, font, text):
            self.baseRect = baseRect
            self.font = font
            self.text = text
        # VERY TEMPORARY RENDERING, I'll make it look better later
        def render(self, screen):
            outlineSize = 5
            innerRect = pygame.Rect(self.baseRect.x + outlineSize, self.baseRect.y + outlineSize, self.baseRect.width - (2 * outlineSize), self.baseRect.height - (2 * outlineSize))
            pygame.draw.rect(screen, 'black', self.baseRect)
            pygame.draw.rect(screen, 'white', innerRect)
            # render text
            textRender = self.font.render(str(self.text), False, 'black')
            scale = min([(innerRect.width - 2 * outlineSize) / textRender.get_width(), (innerRect.height - 2 * outlineSize) / textRender.get_height()])
            textRender = pygame.transform.scale_by(textRender, scale)
            textRect = textRender.get_rect(center=innerRect.center)
            screen.blit(textRender, textRect)
        def setRect(self, rect):
            self.baseRect = rect
        def getClicked(self, mx, my):
            return self.baseRect.collidepoint(mx, my)
    def getRecyclerViewWidthHeightAndPosition(screen):
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        rvHeight = round((screenHeight / 11) * 5)
        rvWidth = (screenWidth // rvHeight) * rvHeight
        # RecyclerView renders in center
        rvX = (screenWidth - rvWidth) // 2
        rvY = (screenHeight - rvHeight) // 2
        return rvWidth, rvHeight, rvX, rvY

    # Creates or updates the screen, to allow for fullscreen
    def createScreen(width, height, fullscreen = False):
        if fullscreen:
            screen = pygame.display.set_mode((width, height), flags=pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((width, height), flags=pygame.RESIZABLE)
        return screen
    # TEMP: just print that level is being played
    def playLevelAtDifficulty(levelNumber, difficulty, playableDifficulties, screen, fullscreen, oldWidth, oldHeight, monitorWidth, monitorHeight, userID):
        levelCompleted = False
        if playableDifficulties[difficulty] >= levelNumber:
            if levelNumber < 2:
                levelCompleted = mainGame.playLevel(levelNumber, difficulty, screen, fullscreen, oldWidth, oldHeight, monitorWidth, monitorHeight)
            else:
                print(f'playing level {levelNumber + 1} at difficulty {difficulty}')
                levelCompleted = True
        else:
            print(f'cannot play level {levelNumber + 1} at difficulty {difficulty}')
        if levelCompleted:
            return updatePlayableAfterLevelCompleted(playableDifficulties, levelNumber, difficulty, userID)
        return playableDifficulties
    def updatePlayableAfterLevelCompleted(previouslyPlayable, levelCompleted, difficultyCompleted, userID):
        levelPlayable = levelCompleted + 1
        for i in range(difficultyCompleted + 1):
            if previouslyPlayable[i] < levelPlayable:
                previouslyPlayable[i] = levelPlayable
        if userID != "-1":
            savePlayableLevels(userID, previouslyPlayable)
        return previouslyPlayable
    def updateButtonSizes(screen, buttons):
        screenWidth = screen.get_width()
        screenHeight = screen.get_height()
        buttonWidth = screenWidth // 4
        buttonHeight = (screenHeight * 2) // 11
        buttonCushion = screenWidth // 16
        buttonX = buttonCushion
        buttonY = (screenHeight * 17) // 22
        for button in buttons:
            button.setRect(pygame.Rect(buttonX, buttonY, buttonWidth, buttonHeight))
            buttonX += (buttonWidth + buttonCushion)
        return buttons
    def loadPlayableLevels(userID):
        if userID == "-1":
            return [0, 0, 0]
        df = pd.read_csv("users.csv")
        userIndex = df.index[df['username'] == userID].tolist()[0]
        playableEasy = df.at[userIndex, 'playableEasy']
        playableNormal = df.at[userIndex, 'playableNormal']
        playableHard = df.at[userIndex, 'playableHard']
        return [playableEasy, playableNormal, playableHard]
    def savePlayableLevels(userID, playable):
        df = pd.read_csv("users.csv")
        userIndex = df.index[df['username'] == userID].tolist()[0]
        df.at[userIndex, 'playableEasy'] = playable[0]
        df.at[userIndex, 'playableNormal'] = playable[1]
        df.at[userIndex, 'playableHard'] = playable[2]
        df.to_csv("users.csv")
    monitorInfo = pygame.display.Info()
    monitorWidth, monitorHeight = monitorInfo.current_w, monitorInfo.current_h

    # Initialise screen
    screenWidth = monitorWidth//2
    screenHeight = monitorHeight//2

    screen = createScreen(screenWidth, screenHeight)
    fullscreen = False
    oldWidth = screenWidth
    oldHeight = screenHeight

    rvWidth, rvHeight, rvX, rvY = getRecyclerViewWidthHeightAndPosition(screen)

    rv = RecyclerView(pygame.Rect(rvX, rvY, rvWidth, rvHeight), rvHeight)
    rvMoveSpeed = 0.01
    # TEMP: set number of levels, TODO: change to load all levels in order of their levelID, and then work out number of levels from there
    totalLevels = 10
    # TEMP: hardcoded, will be found from csv
    # playableDifficulties [10, 8, 6] means that level 11 can be played on easy, level 9 can be played on normal, level 7 can be played on hard. I gave them with index start of 0
    playableDifficulties = loadPlayableLevels(userID)
    levelInfo = [{
        'font': pygame.font.Font('assets/upheavtt.ttf', 32),
        'levelNumber': i + 1,
        'easyCompleted': playableDifficulties[0] > i,
        'normalCompleted': playableDifficulties[1] > i,
        'hardCompleted': playableDifficulties[2] > i
    } for i in range(totalLevels)]
    # populate the RecyclerView
    rv.populate(levelInfo)
    # setup the buttons
    buttons = updateButtonSizes(screen, [Button(pygame.Rect(0, 0, 0, 0), pygame.font.Font('assets/upheavtt.ttf', 32), difficulty) for difficulty in ['EASY', 'NORMAL', 'HARD']])
    # initialise the level as -1, none selected
    levelSelected = -1
    running = True
    while running:
        updateRvSize = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.WINDOWSIZECHANGED:
                screenWidth = screen.get_width()
                screenHeight = screen.get_height()
                updateRvSize = True
            if event.type == pygame.MOUSEBUTTONUP:
                mx, my = pygame.mouse.get_pos()
                buttonClicked = False
                if levelSelected > -1:
                    for buttonI, button in enumerate(buttons):
                        if button.getClicked(mx, my):
                            playableDifficulties = playLevelAtDifficulty(levelSelected, buttonI, playableDifficulties, screen, fullscreen, oldWidth, oldHeight, monitorWidth, monitorHeight, userID)
                            rv.updateDifficulties(playableDifficulties)
                            updateRvSize = True
                            buttonClicked = True
                            break
                if not(buttonClicked):
                    levelSelected = rv.getIndexClicked(mx, my)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    fullscreen = not(fullscreen)
                    if fullscreen:
                        oldWidth = screenWidth
                        oldHeight = screenHeight
                        screen = createScreen(monitorWidth, monitorHeight, fullscreen)
                    else:
                        screen = createScreen(oldWidth, oldHeight, fullscreen)
                    updateRvSize = True
        # temp: just use arrow keys/wasd to move around recyclerview. TODO: mouse support.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            rv.changeT(rvMoveSpeed)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            rv.changeT(-1 * rvMoveSpeed)
        # update recyclerview size if needed
        if updateRvSize:
            rvWidth, rvHeight, rvX, rvY = getRecyclerViewWidthHeightAndPosition(screen)
            rv.setRenderRect(pygame.Rect(rvX, rvY, rvWidth, rvHeight))
            rv.setItemWidth(rvHeight)
            buttons = updateButtonSizes(screen, buttons)
        # render screen
        screen.fill('gray')
        # display recyclerview
        rv.render(screen)
        # if a level is selected, display buttons
        if levelSelected > -1:
            for button in buttons:
                button.render(screen)
        pygame.display.flip()

if __name__ == '__main__':
    selectLevel("-1")