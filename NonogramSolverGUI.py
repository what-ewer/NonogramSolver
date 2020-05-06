import pygame
pygame.init()

# Grid do wyświetlania pełnej planszy
class Grid:

    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.holes = [[Hole(x, y, width, height) for x in range(cols)] for y in range(rows)]
        self.width = width
        self.height = height
        self.window = window
        self.sGap = 20
        self.hintsHeight = 100
        self.hintsWidth = 100
        self.wGap = (self.width - self.hintsWidth - self.sGap) / self.cols
        self.hGap = (self.height - self.hintsHeight - self.sGap) / self.rows

    def draw(self):
        # Rysowanie siatki
        thickness = 2

        for i in range (self.cols + 1):
            pygame.draw.line(self.window, (0,0,0), (self.hintsWidth, self.hintsHeight + i * self.wGap), (self.height - self.sGap, self.hintsHeight + i * self.wGap), thickness)

        for i in range (self.rows + 1):
            pygame.draw.line(self.window, (0,0,0), (self.hintsWidth + i * self.hGap, self.hintsHeight), (self.hintsWidth + i * self.hGap, self.width - self.sGap), thickness)
        
        # Rysowanie dziur
        for x in range(self.rows):
            for y in range(self.cols):
                self.holes[x][y].draw(self.window, self.rows, self.cols, self.hintsWidth, self.hintsHeight, self.sGap)

    def refresh(self):
        self.window.fill((255,255,255))
        self.draw()

    def click(self, mousePosition):
        (x, y) = mousePosition

        if x < self.hintsWidth or y < self.hintsHeight:
            return

        if x > self.width - self.sGap or y > self.height - self.sGap:
            return

        (x, y) = (x - self.hintsWidth, y - self.hintsHeight)

        col = int(x // self.wGap)
        row = int(y // self.hGap)

        hole = self.getHole(row, col)
        hole.inc()

    def getHole(self, row, col):
        for holesList in self.holes:
            for h in holesList:
                if h.row == row and h.col == col:
                    return h
        return None


# Hint do pojedynczej wskazówki
class Hint:
    None

# Hole do pojedynczej dziury
class Hole:

    def __init__(self, row, col, width, height):
        self.value = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
    
    def draw(self, window, rows, cols, hW, hH, sGap):

        if self.value % 3 == 0:
            # Brak zapełnienia
            pass
        elif self.value % 3 == 1:
            # Zapełnienie czarnym kolorem
            wGap = (self.width - hW - sGap) / cols
            hGap = (self.height - hH - sGap) / rows
            pygame.draw.rect(window, (0, 0, 0), (hW + self.col * hGap + 3, hH + self.row * wGap + 3, hGap - 4, wGap - 4), 0)
        else: 
            # Zapełnienie X / szarym
            wGap = (self.width - hW - sGap) / cols
            hGap = (self.height - hH - sGap) / rows
            pygame.draw.rect(window, (200, 200, 200), (hW + self.col * hGap + 3, hH + self.row * wGap + 3, hGap - 4, wGap - 4), 0)
            #pygame.draw.line(window, (0,0,0), (hW + self.col * hGap, hH + self.row * wGap), (hW + (self.col + 1) * hGap, hH + (self.row + 1) * wGap), 3)
            #pygame.draw.line(window, (0,0,0), (hW + (self.col + 1) * hGap, hH + self.row * wGap), (hW + self.col * hGap, hH + (self.row + 1) * wGap), 3)
    
    def inc(self):
        self.value += 1
    
if __name__ == "__main__":
    window = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("NonogramSolver")
    nonogramBoard = Grid(15, 15, 600, 600, window)
    run = True
    
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                print(mousePosition)
                nonogramBoard.click(mousePosition)

        nonogramBoard.refresh()
        pygame.display.update()

    pygame.quit()