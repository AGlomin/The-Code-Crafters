# Deals with loading and saving levels.
"""
Level file follows the following format
Line 1: rows, columns, Brawler Row, Brawler Column, Bomber Row, Bomber Column, Medic Row, Medic Column, (Obstacle Row, Obstacle Column)*
Line 2, 3, 4: (Enemy ID, Enemy Row, Enemy Column)*

Line 1 is used for the base layout of the level, lines 2-4 are the 3 stages within the level
"""
# Get stage information
def getStageInformation(stageBase):
    stageInfo = []
    for i in range(0, len(stageBase), 3):
        try:
            stageInfo.append([stageBase[i], int(stageBase[i+1]), int(stageBase[i+2])])
        except:
            continue
    return stageInfo
# Load level
def loadLevel(fileName: str):
    with open(fileName) as file:
        lines = [line.strip() for line in file]
        # Base Layout
        baseLayout = lines[0].replace(" ","").split(',')
        rows = int(baseLayout[0])
        cols = int(baseLayout[1])
        brawlerRow = int(baseLayout[2])
        brawlerCol = int(baseLayout[3])
        bomberRow = int(baseLayout[4])
        bomberCol = int(baseLayout[5])
        medicRow = int(baseLayout[6])
        medicCol = int(baseLayout[7])
        obstacleInfo = baseLayout[8:]
        obstaclePlaces = []
        for i in range(0, len(obstacleInfo), 2):
            try:
                obstaclePlaces.append([int(obstacleInfo[i]), int(obstacleInfo[i+1])])
            except:
                continue
        # Stages
        stages = [getStageInformation(stage.replace(" ","").split(',')) for stage in lines[1:]]
        return rows, cols, brawlerRow, brawlerCol, bomberRow, bomberCol, medicRow, medicCol, obstaclePlaces, stages
    