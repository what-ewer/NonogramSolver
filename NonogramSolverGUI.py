from HintParser import HintParser
from NonogramSolver import NonogramSolver
import pygame

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
        self.hintsHeight = self.topHints * MainWindow.DSIZE
        self.hintsWidth = self.leftHints * MainWindow.DSIZE
        self.solver = solver
        self.holes = [[Hole(x, y, width, height) for x in range(rows)] for y in range(cols)]
        self.hints = self.__getHints__(hints)
        self.solved = False
        self.solution = []

    def draw(self):
        # Rysowanie siatki
        thickness = 2
        for i in range (self.rows + 1):
            pygame.draw.line(self.window, MainWindow.BLACK, (self.hintsWidth, self.hintsHeight + i * MainWindow.DSIZE), (self.width - MainWindow.sGap, self.hintsHeight + i * MainWindow.DSIZE), thickness)
        for i in range (self.cols + 1):
            pygame.draw.line(self.window, MainWindow.BLACK, (self.hintsWidth + i * MainWindow.DSIZE, self.hintsHeight), (self.hintsWidth + i * MainWindow.DSIZE, self.height - MainWindow.sGap), thickness)

        # Rysowanie Solve i Reset
        fSize = int(MainWindow.DSIZE/2)
        font = pygame.font.SysFont("arialblack", fSize)
        pygame.draw.rect(self.window, MainWindow.GREEN, (0, 0, self.hintsWidth, self.hintsHeight/2), 0)
        text = font.render("SOLVE", 1, MainWindow.BLACK)
        self.window.blit(text, ((self.hintsWidth - 40)/2, self.hintsHeight/4 - fSize / 2))
        pygame.draw.rect(self.window, MainWindow.RED, (0, self.hintsHeight/2, self.hintsWidth, self.hintsHeight/2), 0)
        text = font.render("RESET", 1, MainWindow.BLACK)
        self.window.blit(text, ((self.hintsWidth - 40)/2, self.hintsHeight*3/4 - fSize / 2))

        # Rysowanie wskazówek
        for h in self.hints:
            h.draw(self.window, self.hintsWidth, self.hintsHeight)
        # Rysowanie dziur
        for x in range(self.rows):
            for y in range(self.cols):
                self.holes[y][x].draw(self.window, self.rows, self.cols, self.hintsWidth, self.hintsHeight)

    # Refreshowanie planszy
    def refresh(self):
        self.window.fill(MainWindow.WHITE)
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
        if x > self.width - MainWindow.sGap or y > self.height - MainWindow.sGap:
            return
        (x, y) = (x - self.hintsWidth, y - self.hintsHeight)
        col = int(x // MainWindow.DSIZE)
        row = int(y // MainWindow.DSIZE)
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
            fSize = int(MainWindow.DSIZE/2)
            font = pygame.font.SysFont("arialblack", fSize)
            text = font.render(str(self.value), 1, MainWindow.BLACK)
            gap = 1
            if self.value // 10:
                gap = 1/2
            # self allignment = góra w przeciwnym wypadku lewa strona
            if self.allignment:
                window.blit(text, (hW + gap * MainWindow.DSIZE/3 + self.rowcol * MainWindow.DSIZE, hH - MainWindow.DSIZE - (self.pos * MainWindow.DSIZE)))
            else:
                window.blit(text, (hW + gap * MainWindow.DSIZE/3 - MainWindow.DSIZE - self.pos * MainWindow.DSIZE, hH + MainWindow.DSIZE/4 + self.rowcol * MainWindow.DSIZE))

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
            wGap = (self.width - hW - MainWindow.sGap) / cols
            hGap = (self.height - hH - MainWindow.sGap) / rows
            pygame.draw.rect(window, MainWindow.BLACK, (hW + self.col * wGap + 3, hH + self.row * hGap + 3, wGap - 4, hGap - 4), 0)
        else: 
            # Zapełnienie X / szarym kolorem
            wGap = (self.width - hW - MainWindow.sGap) / cols
            hGap = (self.height - hH - MainWindow.sGap) / rows
            pygame.draw.rect(window, MainWindow.GRAY, (hW + self.col * wGap + 3, hH + self.row * hGap + 3, wGap - 4, hGap - 4), 0)
            # Zapełnienie X
            #pygame.draw.line(window, MainWindow.BLACK, (hW + self.col * hGap, hH + self.row * wGap), (hW + (self.col + 1) * hGap, hH + (self.row + 1) * wGap), 3)
            #pygame.draw.line(window, MainWindow.BLACK, (hW + (self.col + 1) * hGap, hH + self.row * wGap), (hW + self.col * hGap, hH + (self.row + 1) * wGap), 3)
    
    def addValue(self, val):
        self.value += val

# Głowne okno
class MainWindow:
    DSIZE = 60
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    GREEN = (0, 128, 0)
    RED = (255, 0, 0)
    sGap = 20

    def __init__(self, path):
        MainWindow.DSIZE = 60
        pygame.init()
        pygame.font.init()
        n, width, height, hints, ts, ls = MainWindow.load_nonogram(path)
        while MainWindow.DSIZE * (width + ls) + MainWindow.sGap > 1920:
            MainWindow.DSIZE -= 2
        while MainWindow.DSIZE * (height + ts) + MainWindow.sGap > 1000:
            MainWindow.DSIZE -= 2
        (w_x, w_y) = (MainWindow.DSIZE * (width + ls) + MainWindow.sGap, MainWindow.DSIZE * (height + ts) + MainWindow.sGap)
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

    @staticmethod
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
    mw = MainWindow("hints/AGH")