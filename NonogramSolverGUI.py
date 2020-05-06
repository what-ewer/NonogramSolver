import pygame
pygame.init()

# Grid do wyświetlania pełnej planszy
class Grid:

    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.holes = [[Hole(x, y, width, height, window, rows, cols) for x in range(cols)] for y in range(rows)]
        self.width = width
        self.height = height
        self.window = window

    def draw(self):
        # Rysowanie siatki
        sGap = 20
        wGap = (self.width - 100 - sGap) / self.cols
        hGap = (self.height - 100 - sGap) / self.rows
        thickness = 2

        for i in range (self.cols + 1):
            pygame.draw.line(self.window, (0,0,0), (100, 100 + i * wGap), (self.height - sGap, 100 + i * wGap), thickness)

        for i in range (self.rows + 1):
            pygame.draw.line(self.window, (0,0,0), (100 + i * hGap, 100), (100 + i * hGap, self.width - sGap), thickness)
        
        # Rysowanie dziur
        for x in range(self.rows):
            for y in range(self.cols):
                self.holes[x][y].draw(self.window)

    def refresh(self):
        self.window.fill((255,255,255))
        self.draw()


# Hint do pojedynczej wskazówki
class Hint:
    None

# Hole do pojedynczej dziury
class Hole:

    def __init__(self, row, col, width, height, window, rows, cols):
        self.value = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.window = window
        self.rows = rows
        self.cols = cols
    
    def draw(self, window):

        if self.value % 3 == 0:
            # Brak zapełnienia
            pass
        elif self.value % 3 == 1:
            # Zapełnienie czarnym kolorem
            sGap = 20
            wGap = (self.width - 100 - sGap) / self.cols
            hGap = (self.height - 100 - sGap) / self.rows
            pygame.draw.rect(self.window, (0, 0, 0), (100 + self.col * hGap, 100 + self.row * wGap, hGap, wGap), 0)
            pass
        else: 
            # Zapełnienie X
            pass
    
if __name__ == "__main__":
    window = pygame.display.set_mode((600,600))
    pygame.display.set_caption("NonogramSolver")
    nonogramBoard = Grid(3, 3, 600, 600, window)
    while True:
        nonogramBoard.refresh()
        pygame.display.update()
    pygame.quit()