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

    def draw(self):
        # Rysowanie siatki
            
        # Rysowanie dziur
        pass

    def refresh(self):
        self.window.fill((255,255,255))
        self.draw()


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
    
    def draw(self, window):

        if self.value % 3 == 0:
            # Brak zapełnienia
            pass
        elif self.value % 3 == 1:
            # Zapełnienie czarnym kolorem
            pass
        else: 
            # Zapełnienie X
            pass
    
if __name__ == "__main__":
    window = pygame.display.set_mode((600,660))
    pygame.display.set_caption("NonogramSolver")
    nonogramBoard = Grid(3, 3, 600, 600, window)
    while True:
        nonogramBoard.refresh()
    pygame.quit()