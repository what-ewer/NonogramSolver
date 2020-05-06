from HintParser import HintParser
from NonogramSolver import NonogramSolver
import pygame

pygame.init()
pygame.font.init()

DSIZE = 40
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
sGap = 20

LOGO = pygame.image.load('logo.png') 

# Grid do wyświetlania pełnej planszy
class Grid:

    def __init__(self, rows, cols, width, height, window, hints, topHints, leftHints, solver):
        self.window = window
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.topHints = topHints
        self.leftHints = leftHints
        self.hintsHeight = self.topHints * DSIZE
        self.hintsWidth = self.leftHints * DSIZE
        self.solver = solver
        self.holes = [[Hole(x, y, width, height) for x in range(rows)] for y in range(cols)]
        self.hints = self.__getHints__(hints)
        self.solved = False
        self.solution = []

    def draw(self):
        # Rysowanie siatki
        thickness = 2

        for i in range (self.rows + 1):
            pygame.draw.line(self.window, BLACK, (self.hintsWidth, self.hintsHeight + i * DSIZE), (self.width - sGap, self.hintsHeight + i * DSIZE), thickness)

        for i in range (self.cols + 1):
            pygame.draw.line(self.window, BLACK, (self.hintsWidth + i * DSIZE, self.hintsHeight), (self.hintsWidth + i * DSIZE, self.height - sGap), thickness)

        # Rysowanie Solve i Reset
        fSize = int(DSIZE/2)
        font = pygame.font.SysFont("arialblack", fSize)

        pygame.draw.rect(window, GREEN, (0, 0, self.hintsWidth, self.hintsHeight/2), 0)
        text = font.render("SOLVE", 1, BLACK)
        window.blit(text, ((self.hintsWidth - 40)/2, self.hintsHeight/4 - fSize / 2))

        pygame.draw.rect(window, RED, (0, self.hintsHeight/2, self.hintsWidth, self.hintsHeight/2), 0)
        text = font.render("RESET", 1, BLACK)
        window.blit(text, ((self.hintsWidth - 40)/2, self.hintsHeight*3/4 - fSize / 2))
        
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
                self.holes[y][x].draw(self.window, self.rows, self.cols, self.hintsWidth, self.hintsHeight)

    # Refreshowanie planszy
    def refresh(self):
        self.window.fill(WHITE)
        self.draw()

    # Handler kliknięcia na plansze
    def click(self, mousePosition, val):
        (x, y) = mousePosition

        if x < self.hintsWidth or y < self.hintsHeight:
            if y < self.hintsHeight/2 and x < self.hintsWidth:
                self.solve()
            elif y < self.hintsHeight and x < self.hintsWidth:
                self.reset()
            return

        if x > self.width - sGap or y > self.height - sGap:
            return

        (x, y) = (x - self.hintsWidth, y - self.hintsHeight)

        col = int(x // DSIZE)
        row = int(y // DSIZE)

        hole = self.__getHole__(row, col)
        hole.addValue(val)

    # Reset wartości dziur
    def reset(self):
        for holesList in self.holes:
            for h in holesList:
                h.value = 0

    # Rozwiązanie 
    def solve(self):
        if not self.solved:
            self.solver.solve()
            self.solution = self.solver.state
            self.solved = True

        for x in range(self.rows):
            for y in range(self.cols):
                self.holes[y][x].value = self.solution[x,y]

    def __getHole__(self, row, col):
        for holesList in self.holes:
            for h in holesList:
                if h.row == row and h.col == col:
                    return h
        return None

    def __getHints__(self, hints):
        return [Hint(hint, i, len(hints[k][i]) - num - 1, k) 
            for k in range(2) for i in range(len(hints[k])) for num, hint in enumerate(hints[k][i])]


# Hint do pojedynczej wskazówki
class Hint:
    def __init__(self, value, rowcol, pos, allignment):
        self.value = value
        self.allignment = allignment
        self.rowcol = rowcol
        self.pos = pos

    def draw(self, window, hW, hH):
        if self.value != 0:
            fSize = int(DSIZE/2)

            font = pygame.font.SysFont("arialblack", fSize)
            text = font.render(str(self.value), 1, BLACK)
            gap = 1
            if self.value // 10:
                gap = 1/2

            # self allignment = góra w przeciwnym wypadku lewa strona
            if self.allignment:
                window.blit(text, (hW + gap * DSIZE/3 + self.rowcol * DSIZE, hH - DSIZE - (self.pos * DSIZE)))
            else:
                window.blit(text, (hW + gap * DSIZE/3 - DSIZE - self.pos * DSIZE, hH + DSIZE/4 + self.rowcol * DSIZE))
    
    

# Hole do pojedynczej dziury
class Hole:

    def __init__(self, row, col, width, height):
        self.value = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
    
    def draw(self, window, rows, cols, hW, hH):

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

    top_size = 3
    left_size = 3
    for i in range(len(n.hints[0])):
        left_size = max(left_size, len(n.hints[0][i]))

    for i in range(len(n.hints[1])):
        top_size = max(top_size, len(n.hints[1][i]))

    return n, n.width, n.height, n.hints, top_size, left_size


if __name__ == "__main__":
    n, width, height, hints, ts, ls = load_nonogram("hints/statek")
    
    while DSIZE * (width + ls) + sGap > 1920:
        DSIZE -= 2
    
    while DSIZE * (height + ts) + sGap > 1000:
        DSIZE -= 2


    (w_x, w_y) = (DSIZE * (width + ls) + sGap, DSIZE * (height + ts) + sGap)
    print(w_x, w_y)
    window = pygame.display.set_mode((w_x, w_y))
    pygame.display.set_caption("NonogramSolver")
    nonogramBoard = Grid(height, width, w_x,  w_y, window, hints, ts, ls, n)
    run = True
    
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    nonogramBoard.solve()
                if event.key == pygame.K_r:
                    nonogramBoard.reset()
            
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