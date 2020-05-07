import pygame
import numpy as np

class Grid:

    def __init__(self, rows, cols, width, height, window, filename):
        self.window = window
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.filename = filename
        self.holes = [[0 for x in range(rows)] for y in range(cols)]

    def draw(self):
        # Rysowanie siatki
        thickness = 2
        for i in range (self.rows + 1):
            pygame.draw.line(self.window, MainWindow.BLACK, (MainWindow.GAP, MainWindow.GAP + i * MainWindow.DSIZE), (self.width - MainWindow.GAP, MainWindow.GAP + i * MainWindow.DSIZE), thickness)
        for i in range (self.cols + 1):
            pygame.draw.line(self.window, MainWindow.BLACK, (MainWindow.GAP + i * MainWindow.DSIZE, MainWindow.GAP), (MainWindow.GAP + i * MainWindow.DSIZE, self.height - MainWindow.GAP), thickness)

        # Rysowanie dziur
        for x in range(self.rows):
            for y in range(self.cols):
                if (self.holes[y][x] % 2 == 1):
                    pygame.draw.rect(self.window, MainWindow.BLACK, (MainWindow.GAP + y * MainWindow.DSIZE + 3, MainWindow.GAP + x * MainWindow.DSIZE + 3, MainWindow.DSIZE - 4, MainWindow.DSIZE - 4), 0)

    # Refreshowanie planszy
    def refresh(self):
        self.window.fill(MainWindow.WHITE)
        self.draw()

    # Zapisanie planszy
    def save(self):
        print("Zamiana obrazka na podpowiedzi i zapisywanie")

        solution = [[], []]
        print(solution)
        print(len(self.holes[0]))

        tmp = 0
        for x in range(self.rows):
            arr = []
            for y in range(self.cols):
                if (self.holes[y][x] % 2 == 1):
                    tmp += 1
                elif tmp != 0:
                    arr.append(tmp)
                    tmp = 0

            if  tmp != 0:
                arr.append(tmp)

            if len(arr) == 0:
                arr.append(tmp)

            solution[0].append(arr)
            tmp = 0

        for x in range(self.cols):
            arr = []
            for y in range(self.rows):
                if (self.holes[x][y] % 2 == 1):
                    tmp += 1
                elif tmp != 0:
                    arr.append(tmp)
                    tmp = 0
            
            if  tmp != 0:
                arr.append(tmp)

            if len(arr) == 0:
                arr.append(0)

            solution[1].append(arr)
            tmp = 0

        f = open(self.filename, mode="w+", encoding="utf-8")
        f.write(str(solution))
        f.close()
        #print(str(solution))


    # Handler kliknięcia na plansze
    def click(self, mousePosition, val):
        (x, y) = mousePosition
        if x < MainWindow.GAP or y < MainWindow.GAP:
            return

        if x > self.width - MainWindow.GAP or y > self.height - MainWindow.GAP:
            return

        (x, y) = (x - MainWindow.GAP, y - MainWindow.GAP)
        col = int(x // MainWindow.DSIZE)
        row = int(y // MainWindow.DSIZE)

        self.holes[col][row] += val

    # Reset wartości dziur
    def reset(self):
        for holesList in self.holes:
            for h in holesList:
                h.value = 0

class MainWindow:
    GAP = 5
    DSIZE = 60
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, width, height, filename):
        MainWindow.DSIZE = 60
        pygame.init()
        pygame.font.init()

        while MainWindow.DSIZE * width + 2 * MainWindow.GAP > 1920:
            MainWindow.DSIZE -= 2
        while MainWindow.DSIZE * height + 2 * MainWindow.GAP > 1000:
            MainWindow.DSIZE -= 2

        (w_x, w_y) = (MainWindow.DSIZE * width + 2 * MainWindow.GAP, MainWindow.DSIZE * height + 2 * MainWindow.GAP)

        window = pygame.display.set_mode((w_x, w_y))

        pygame.display.set_caption("NonogramMakerImage")
        nonogramBoard = Grid(height, width, w_x,  w_y, window, filename)
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        nonogramBoard.save()
                    if event.key == pygame.K_r:
                        nonogramBoard.reset()   
                    if event.key == pygame.K_e:
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

if __name__ == "__main__":
    nmi = MainWindow(10, 5, "test")