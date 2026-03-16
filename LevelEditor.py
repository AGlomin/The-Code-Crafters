import pygame
import LevelHandler
# trying to understand my code here is like trying to decipher ancient heiroglyphics so I will need to add comments once this is more functional
# screen class
class Screen:
    def __init__ (self, width, height, bg_colour, side_size = 0):
        self.width = width
        self.height = height
        self.side_size = side_size
        self.surface = pygame.display.set_mode((width, height))
        self.bg_colour = bg_colour
    def blit(self, surface, position):
        self.surface.blit(surface, position)
    def get_width(self):
        return self.width - self.side_size
    def get_height(self):
        return self.height
    def get_center(self):
        return ((self.width-self.side_size)//2,self.height//2)
    def get_surface(self):
        return self.surface
    def render_background(self):
        self.surface.fill(self.bg_colour)
    def show_screen(self):
        pygame.display.flip()
# single tile in Level
class GridSquare:
    def __init__(self, pos, gridSize, state, imageBase, imageObstacle, imageEnemy, screen, min_cushion_size=1.5, start = False):
        rows, cols = gridSize
        self.size = min(screen.get_width()//cols, screen.get_height()//rows)
        self.state = state
        self.imageBase = imageBase
        self.imageObstacle = imageObstacle
        self.imageEnemy = imageEnemy
        self.min_cushion_size = min_cushion_size
        row, col = pos
        cx, cy = screen.get_center()
        self.x = round(cx + (self.size * (col + 1 - ((cols + 1)/2))))
        self.y = round(cy - (self.size * (((rows + 1)/2) - row - 1)))
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_size(self):
        return self.size
    def get_state(self):
        return self.state
        # to allow grid to fit on screen
    def set_state(self, state, enemyImage = None):
        self.state = state
        self.imageEnemy = enemyImage
    def grid_rescale(self, pos, gridSize, screen):
        rows, cols = gridSize
        self.size = min(screen.get_width()//cols, screen.get_height()//rows)
        row, col = pos
        cx, cy = screen.get_center()
        self.x = round(cx + (self.size * (col + 1 - ((cols + 1)/2))))
        self.y = round(cy - (self.size * (((rows + 1)/2) - row - 1)))
    def render(self, screen):
        base = self.imageBase.copy()
        if self.state == '1':
            base.blit(self.imageObstacle,(0,0))
        elif self.state != '0':
            base.blit(self.imageEnemy, (0,0))
        final_size = min(round((1- (2 * 0.01)) * self.size), self.size - 2 * self.min_cushion_size)
        baseResized = pygame.transform.scale(base, (final_size, final_size))
        rect = pygame.Rect(0, 0, final_size, final_size)
        rect.center = (self.x, self.y)
        screen.blit(baseResized, rect)
    def check_collision(self, mx, my):
        final_size = min(round((1- (2 * 0.01)) * self.size), self.size - 2 * self.min_cushion_size)
        rect = pygame.Rect(0, 0, final_size, final_size)
        rect.center = (self.x, self.y)
        return rect.collidepoint(mx, my), mx>(self.x+final_size//2)-1, my>(self.y+final_size//2)-1
# Level class used in editor
class Level:
    def __init__(self, Level_arr, screen):
        self.Level_rows = len(Level_arr)
        self.Level_cols = len(Level_arr[0])
        self.Level_squares = [[GridSquare((row, col), (self.Level_rows, self.Level_cols), Level_arr[row][col], pygame.image.load('assets/tile.png'), pygame.image.load('assets/obstacle.png'), None if Level_arr[row][col] == '0' or Level_arr[row][col] == '1' else pygame.image.load(f"assets/{Level_arr[row][col]}.png"), screen, start = (Level_arr[row][col]=='2')) for col in range(self.Level_cols)] for row in range(self.Level_rows)]
        self.start_row = -1
        self.start_col = -1
        """
        for row_index in range(len(Level_arr)):
            row = Level_arr[row_index]
            if '2' in row:
                self.start_row = row_index
                self.start_col = row.index('2')
        """
    def render(self, screen, mx, my, addMode):
        for row in self.Level_squares:
            for col in row:
                col.render(screen)
        self.draw_editor(mx, my, screen, addMode)
    def update_sizes(self, screen):
        for row_index in range(len(self.Level_squares)):
            for col_index in range(len(self.Level_squares[row_index])):
                self.Level_squares[row_index][col_index].grid_rescale((row_index, col_index), (self.Level_rows, self.Level_cols), screen)
    def insert_row(self, row_index, screen):
        self.Level_rows+=1
        self.Level_squares.insert(row_index, [GridSquare((row_index, col), (self.Level_rows, self.Level_cols), '0', pygame.image.load('assets/tile.png'), pygame.image.load('assets/obstacle.png'),None, screen) for col in range(self.Level_cols)])
        self.update_sizes(screen)
    def insert_col(self, col_index, screen):
        self.Level_cols+=1
        for row in range(len(self.Level_squares)):
            self.Level_squares[row].insert(col_index, GridSquare((row, col_index), (self.Level_rows, self.Level_cols), '0', pygame.image.load('assets/tile.png'), pygame.image.load('assets/obstacle.png'),None, screen))
        self.update_sizes(screen)
    def delete_row(self, row_index, screen):
        if self.Level_rows!=1:
            self.Level_rows-=1
            self.Level_squares.pop(row_index)
            self.update_sizes(screen)
    def delete_col(self, col_index, screen):
        if self.Level_cols!=1:
            self.Level_cols-=1
            for row in range(len(self.Level_squares)):
                self.Level_squares[row].pop(col_index)
            self.update_sizes(screen)
    def find_collision(self, mx, my):
        # return square, row, col
        x = []
        y = []
        for row_index in range(len(self.Level_squares)):
            x_row = []
            y_row = []
            for col_index in range(len(self.Level_squares[row_index])):
                square = self.Level_squares[row_index][col_index]
                square_collision, right, below = square.check_collision(mx, my)
                if square_collision:
                    return True, row_index, col_index
                x_row.append(right)
                y_row.append(below)
            x.append(x_row)
            y.append(y_row)
        # find where x (col) differs
        col_differ = len(x[0])
        for i in range(len(x[0])):
            if not(x[0][i]):
                col_differ = i
                break
        # find where y (row) differs
        row_differ = len(y)
        for i in range(len(y)):
            if not(y[i][0]):
                row_differ = i
                break
        return False, row_differ, col_differ
    # over-complicated code just for editing the Level (changing state, or adding/removing rows/columns, depending on the mode and where clicked)
    def Level_click(self, mx, my, screen, addMode):
        square, row, col = self.find_collision(mx, my)
        # square clicked
        if square:
            # temp, make enemy 1
            if self.Level_squares[row][col].get_state() == '0':
                self.setEnemy('en1', row, col)
            else:
                self.removeEnemy(row, col)
        else:
            size = self.Level_squares[0][0].get_size()
            screen_width, screen_height = screen.get_width(), screen.get_height()
            if row == self.Level_rows:
                square_row = row-1
                draw_row = size
            else:
                square_row = row
                draw_row = 0
            if col == self.Level_cols:
                square_col = col-1
                draw_col = size
            else:
                square_col = col
                draw_col = 0
            draw_row += self.Level_squares[square_row][0].get_y()-size//2
            draw_col += self.Level_squares[0][square_col].get_x()-size//2
            cx, cy = self.Level_squares[square_row][square_col].get_x(),self.Level_squares[square_row][square_col].get_y()
            if row == self.Level_rows:
                square_row +=1
            if col == self.Level_cols:
                square_col +=1
            if addMode:
                if abs(mx-screen_width//2)>self.Level_squares[-1][-1].get_x()-screen_width//2+size//2:
                    self.insert_col(square_col, screen)
                elif abs(my-screen_height//2)>self.Level_squares[-1][-1].get_y()-screen_height//2+size//2:
                    self.insert_row(square_row, screen)
                elif abs(cx-mx)<abs(cy-my):
                    self.insert_row(square_row, screen)
                else:
                    self.insert_col(square_col, screen)
            else:
                if abs(mx-screen_width//2)>self.Level_squares[-1][-1].get_x()-screen_width//2+size//2:
                    self.delete_row(square_row, screen)
                elif abs(my-screen_height//2)>self.Level_squares[-1][-1].get_y()-screen_height//2+size//2:
                    self.delete_col(square_col, screen)
                elif abs(cx-mx)<abs(cy-my):
                    self.delete_col(square_col, screen)
                else:
                    self.delete_row(square_row, screen)
        try:
            if self.Level_squares[self.start_row][self.start_col].get_state()!='2':
                self.start_row = -1
                self.start_col = -1
        except:
            self.start_row = -1
            self.start_col = -1
    # drawing the editor. Highlights square, row or column that is being hovered over
    def draw_editor(self, mx, my, screen, addMode):
        square, row, col = self.find_collision(mx, my)
        size = self.Level_squares[0][0].get_size()
        if square:
            thisSquare = self.Level_squares[row][col]
            rect = pygame.Rect((0,0),(size,size))
            rect.center = (thisSquare.get_x(), thisSquare.get_y())
            pygame.draw.rect(screen.get_surface(), 'green',rect, width = 2)
        else:
            screen_width, screen_height = screen.get_width(), screen.get_height()
            if row == self.Level_rows:
                square_row = row-1
                draw_row = size
            else:
                square_row = row
                draw_row = 0
            if col == self.Level_cols:
                square_col = col-1
                draw_col = size
            else:
                square_col = col
                draw_col = 0
            draw_row += self.Level_squares[square_row][0].get_y()-size//2
            draw_col += self.Level_squares[0][square_col].get_x()-size//2
            cx, cy = self.Level_squares[square_row][square_col].get_x(),self.Level_squares[square_row][square_col].get_y()
            if row == self.Level_rows:
                square_row +=1
            if col == self.Level_cols:
                square_col +=1
            if addMode:
                if abs(mx-screen_width//2)>self.Level_squares[-1][-1].get_x()-screen_width//2+size//2:
                    pygame.draw.line(screen.get_surface(), 'green', (draw_col, 0), (draw_col, screen_height), width = 2)
                elif abs(my-screen_height//2)>self.Level_squares[-1][-1].get_y()-screen_height//2+size//2:
                    pygame.draw.line(screen.get_surface(), 'green', (0, draw_row), (screen_width, draw_row), width = 2)
                elif abs(cx-mx)<abs(cy-my):
                    pygame.draw.line(screen.get_surface(), 'green', (0, draw_row), (screen_width, draw_row), width = 2)
                else:
                    pygame.draw.line(screen.get_surface(), 'green', (draw_col, 0), (draw_col, screen_height), width = 2)
            else:
                if abs(mx-screen_width//2)>self.Level_squares[-1][-1].get_x()-screen_width//2+size//2:
                    pygame.draw.rect(screen.get_surface(), 'red', ((0, draw_row), (screen_width, size)), width = 2)
                elif abs(my-screen_height//2)>self.Level_squares[-1][-1].get_y()-screen_height//2+size//2:
                    pygame.draw.rect(screen.get_surface(), 'red', ((draw_col, 0), (size, screen_height)), width = 2)
                elif abs(cx-mx)<abs(cy-my):
                    pygame.draw.rect(screen.get_surface(), 'red', ((draw_col, 0), (size, screen_height)), width = 2)
                else:
                    pygame.draw.rect(screen.get_surface(), 'red', ((0, draw_row), (screen_width, size)), width = 2)
    # for saving Level
    def get_info(self):
        #Level_arr = []
        enemyArr = []
        for rowI in range(len(self.Level_squares)):
            row = self.Level_squares[rowI]
            #Level_row = []
            for colI in range(len(row)):
                col = row[colI]
                col_state = col.get_state()
                #Level_row.append(col_state if col_state == '1' else '0')
                if col_state != '1' and col_state != '0':
                    enemyArr.extend([col_state, str(rowI), str(colI)])
            #Level_arr.append(''.join(Level_row))
        return ', '.join(enemyArr)
    def setEnemy(self, enemyId, enemyRow, enemyColumn):
        self.Level_squares[enemyRow][enemyColumn].set_state(enemyId, pygame.image.load(f'assets/{enemyId}Proto.png'))
    def removeEnemy(self, row, column):
        self.Level_squares[row][column].set_state('0', None)
    def getRowsAndColumns(self):
        return self.Level_rows, self.Level_cols
# button class
class Button:
    def __init__(self, screen, size, colour, text_colour, side_size, y, font = None, fontsize = 32, text = ""):
        self.text = text
        self.size = size
        self.colour = pygame.Color(colour)
        self.text_colour= pygame.Color(text_colour)
        x = side_size//2
        cx, cy = screen.get_center()
        self.x = screen.get_width() + x
        self.y = cy - y
        self.font = pygame.font.Font(font, fontsize)
    def set_text(self, text):
        self.text = text
    def render(self, screen):
        txt_surface = self.font.render(self.text, True, self.text_colour)
        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = (self.x, self.y)
        pygame.draw.rect(screen.get_surface(), self.colour, rect)
        rect = txt_surface.get_rect()
        rect.center = (self.x, self.y) # since x and y is the center of the button
        screen.surface.blit(txt_surface, rect)
    def check_click(self, mx, my):
        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = (self.x, self.y)
        return rect.collidepoint(mx, my)

pygame.init()

myScreen = Screen(750,500,'black', 100)
buttons = [Button(myScreen, 90, '#00D900', '#002600',100,150 - 100 * i, text = str(i)) for i in range(4)] 
addMode = False
# change mode depending on what mode currently on
def update_add():
    global addMode
    addMode = not(addMode)
    if addMode:
        buttons[0].set_text("Add")
    else:
        buttons[0].set_text("Del")
update_add()
# Add obstacles to level base. Enemies added afterwards
def generateStageWithObstacles(rows, cols, obstaclePlaces):
    baseLevel = [['0' for col in range(cols)] for row in range(rows)]
    for place in obstaclePlaces:
        baseLevel[place[0]][place[1]] = '1'
    return [''.join(row) for row in baseLevel]
# loads level from file. If not there, creates blank level
def load_level_from_file(filename):
    try:
        with open(filename) as file:
            rows, cols, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol, obstaclePlaces, stages = LevelHandler.loadLevel(filename)
            base = generateStageWithObstacles(rows, cols, obstaclePlaces)
            levels = [Level(base[:], myScreen) for i in range(3)]
            # Add enemies
            for stageI in range(3):
                try:
                    stage = stages[stageI]
                except:
                    stage = []
                for enemy in stage:
                    levels[stageI].setEnemy(enemy[0], int(enemy[1]), int(enemy[2]))
            return levels, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol
    except:
        base = generateStageWithObstacles(3, 4, [])
        levels = [Level(base.copy(), myScreen) for i in range(3)]
        return levels, 0, 0, 1, 0, 2, 0
# loads stage from all levels
def load_stage(stageNum, allLevels):
    return allLevels[stageNum - 1], stageNum
# saves Level
def saveStages(allLevels, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol, filename):
    rows, columns = allLevels[0].getRowsAndColumns()
    #obstacles = allLevels[0].getObstacles()
    obstacles = ''
    lines = [', '.join([str(rows), str(columns), str(brawlerRow), str(brawlerCol), str(bomberRow), str(bomberCol), str(medicRow), str(medicCol), obstacles])]
    for i in range(3):
        lines.append(allLevels[i].get_info())
    with open(filename, 'w') as file:
        file.write('\n'.join(lines))
# Render the player characters
def renderPlayers(myScreen, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol):
    
    return
filename = 'test.txt'
levels, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol = load_level_from_file(filename)
myLevel, stageNum = load_stage(1, levels)
running = True
while running:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if buttons[0].check_click(mx, my):
                update_add()
            elif buttons[1].check_click(mx, my):
                myLevel, stageNum = load_stage(1, levels)
            elif buttons[2].check_click(mx, my):
                myLevel, stageNum = load_stage(2, levels)
            elif buttons[3].check_click(mx, my):
                myLevel, stageNum = load_stage(3, levels)
            else:
                myLevel.Level_click(mx, my, myScreen, addMode)
                # save_Level(myLevel, LevelIndex) <- only to run upon close now
    myScreen.render_background()
    myLevel.render(myScreen, mx, my, addMode)
    renderPlayers(myScreen, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol)
    for button in buttons:
        button.render(myScreen)
    myScreen.show_screen()
# Save stages
saveStages(levels, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol, filename)
pygame.quit()
