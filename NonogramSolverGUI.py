from HintParser import HintParser
from NonogramSolver import NonogramSolver
import pygame

pygame.init()
pygame.font.init()

DEFAULT_SIZE = 25
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

LOGO = pygame.image.load('logo.png') 

# Grid do wyświetlania pełnej planszy
class Grid:

    def __init__(self, rows, cols, width, height, window, hints, topHints, leftHints, solver):
        self.window = window
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.topHints = max(3, topHints)
        self.leftHints = max(3, leftHints)
        self.hintsHeight = self.topHints * DEFAULT_SIZE
        self.hintsWidth = self.leftHints * DEFAULT_SIZE
        self.solver = solver
        self.sGap = 20
        self.holes = [[Hole(x, y, width, height) for x in range(rows)] for y in range(cols)]
        self.hints = self.__getHints__(hints)
        self.wGap = (self.width - self.hintsWidth - self.sGap) / self.cols
        self.hGap = (self.height - self.hintsHeight - self.sGap) / self.rows

    def draw(self):
        # Rysowanie siatki
        thickness = 2

        for i in range (self.rows + 1):
            pygame.draw.line(self.window, BLACK, (self.hintsWidth, self.hintsHeight + i * self.hGap), (self.width - self.sGap, self.hintsHeight + i * self.hGap), thickness)

        for i in range (self.cols + 1):
            pygame.draw.line(self.window, BLACK, (self.hintsWidth + i * self.wGap, self.hintsHeight), (self.hintsWidth + i * self.wGap, self.height - self.sGap), thickness)
        
        # Rysowanie logo
        #self.window.blit(LOGO, ((self.hintsWidth - 100) / 2, (self.hintsHeight - 100) / 2)) 
        #pygame.draw.line(self.window, BLACK, (0, self.hintsHeight), (self.hintsWidth, self.hintsHeight), thickness * 2)
        #pygame.draw.line(self.window, BLACK, (self.hintsWidth, self.hintsHeight), (self.hintsWidth, 0), thickness * 2)
        #pygame.draw.line(self.window, BLACK, (0, 0), (self.hintsWidth, 0), thickness * 3)
        #pygame.draw.line(self.window, BLACK, (0, 0), (0, self.hintsHeight), thickness * 3)

        # Rysowanie wskazówek
        for h in self.hints:
            h.draw(self.window, self.hintsWidth, self.hintsHeight)


        # Rysowanie dziur
        for x in range(self.rows):
            for y in range(self.cols):
                self.holes[y][x].draw(self.window, self.rows, self.cols, self.hintsWidth, self.hintsHeight, self.sGap)

    # Refreshowanie planszy
    def refresh(self):
        self.window.fill(WHITE)
        self.draw()

    # Handler kliknięcia na plansze
    def click(self, mousePosition, val):
        (x, y) = mousePosition

        if x < self.hintsWidth or y < self.hintsHeight:
            return

        if x > self.width - self.sGap or y > self.height - self.sGap:
            return

        (x, y) = (x - self.hintsWidth, y - self.hintsHeight)

        col = int(x // self.wGap)
        row = int(y // self.hGap)

        hole = self.__getHole__(row, col)
        hole.addValue(val)

    # Reset wartości dziur
    def reset(self):
        for holesList in self.holes:
            for h in holesList:
                h.value = 0

    # Rozwiązanie 
    def solve(self):
        None

    def __getHole__(self, row, col):
        for holesList in self.holes:
            for h in holesList:
                if h.row == row and h.col == col:
                    return h
        return None

    def __getHints__(self, hints):
        
        h = [Hint(hint, i, len(hints[k][i]) - num - 1, k, self.hintsWidth / self.leftHints, self.hintsHeight / self.topHints) 
            for k in range(2) for i in range(len(hints[0])) for num, hint in enumerate(hints[k][i])]
        
        print(h)

        #h = [Hint(3, 0, 1, True, self.hintsWidth/self.leftHints, self.hintsHeight/self.topHints),
        #     Hint(4, 0, 0, True, self.hintsWidth/self.leftHints, self.hintsHeight/self.topHints),
        #     Hint(5, 0, 2, True, self.hintsWidth/self.leftHints, self.hintsHeight/self.topHints),
        #     Hint(6, 0, 1, False, self.hintsWidth/self.leftHints, self.hintsHeight/self.topHints),
        #     Hint(7, 0, 0, False, self.hintsWidth/self.leftHints, self.hintsHeight/self.topHints)]
        #print(h)
        return h


# Hint do pojedynczej wskazówki
class Hint:
    def __init__(self, value, rowcol, pos, allignment, width, height):
        self.value = value
        self.allignment = allignment
        self.rowcol = rowcol
        self.pos = pos
        self.width = int(width)
        self.height = int(height)

    def draw(self, window, hW, hH):
        if self.value != 0:
            fSize = int(min(self.height, self.width) * 2/3)

            font = pygame.font.SysFont("comicsans", fSize)
            text = font.render(str(self.value), 1, BLACK)

            # self allignment = góra w przeciwnym wypadku lewa strona
            if self.allignment:
                window.blit(text, (hW + self.width/2 + self.rowcol * self.width - fSize/4, hH - self.height/2 - (self.pos * self.height) - fSize/4))
            else:
                window.blit(text, (hW - self.width/2 - self.pos * self.width - fSize/4, hH + self.height/2 + self.rowcol * self.height - fSize/4))
    
    

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
            pygame.draw.rect(window, BLACK, (hW + self.col * wGap + 3, hH + self.row * hGap + 3, wGap - 4, hGap - 4), 0)
        else: 
            # Zapełnienie X / szarym kolorem
            wGap = (self.width - hW - sGap) / cols
            hGap = (self.height - hH - sGap) / rows
            pygame.draw.rect(window, GRAY, (hW + self.col * wGap + 3, hH + self.row * hGap + 3, wGap - 4, hGap - 4), 0)
            # Zapełnienie X
            #pygame.draw.line(window, BLACK, (hW + self.col * hGap, hH + self.row * wGap), (hW + (self.col + 1) * hGap, hH + (self.row + 1) * wGap), 3)
            #pygame.draw.line(window, BLACK, (hW + (self.col + 1) * hGap, hH + self.row * wGap), (hW + self.col * hGap, hH + (self.row + 1) * wGap), 3)
    
    def addValue(self, val):
        self.value += val
    
def load_nonogram(path):
    n = NonogramSolver(HintParser.parseFile(path))

    top_size = 0
    left_size = 0
    for i in range(len(n.hints[0])):
        left_size = max(left_size, len(n.hints[0][i]))

    for i in range(len(n.hints[1])):
        top_size = max(top_size, len(n.hints[1][i]))

    return n, n.width, n.height, n.hints, top_size, left_size


if __name__ == "__main__":
    n, width, height, hints, ts, ls = load_nonogram("hints/AGH")
    (w_x, w_y) = (DEFAULT_SIZE * width, DEFAULT_SIZE * height)
    window = pygame.display.set_mode((w_x, w_y))
    pygame.display.set_caption("NonogramSolver")
    nonogramBoard = Grid(height, width, w_x,  w_y, window, hints, ts, ls, n)
    run = True
    
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                inc = 0
                if event.button == 3:
                    inc = -1
                else:
                    inc = 1

                mousePosition = pygame.mouse.get_pos()
                #print(mousePosition)
                nonogramBoard.click(mousePosition, inc)

        nonogramBoard.refresh()
        pygame.display.update()

    pygame.quit()