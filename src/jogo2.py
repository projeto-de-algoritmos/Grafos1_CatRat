import pygame
import random
import numpy as np

# Define as constantes do tamanho do mapa
WIDTH = 600
HEIGHT = 600
ROWS = 20
COLS = 20
CELL_SIZE = WIDTH // ROWS

# Inicializa a tela do Pygame
pygame.init()

# Cria a janela do jogo
pygame.display.set_caption("Catch Rat")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define as cores do labirinto
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Função find, que busca recursivamente o conjunto ao qual um nó pertence no conjunto de conjuntos de Kruskal
def find(subsets, i):
    if subsets[i] != i:
        subsets[i] = find(subsets, subsets[i])
    return subsets[i]

# Função union, que une dois conjuntos no conjunto de conjuntos de Kruskal
def union(subsets, ranks, x, y):
    xroot = find(subsets, x)
    yroot = find(subsets, y)
 
    if ranks[xroot] < ranks[yroot]:
        subsets[xroot] = yroot
    elif ranks[xroot] > ranks[yroot]:
        subsets[yroot] = xroot
    else:
        subsets[yroot] = xroot
        ranks[xroot] += 1

# Define a classe Cell para representar cada célula do labirinto
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw(self):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.walls['top']:
            pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_SIZE), 2)

    def remove_wall(self, other):
        if self.row == other.row and self.col == other.col + 1:
            self.walls['left'] = False
            other.walls['right'] = False
        elif self.row == other.row and self.col == other.col - 1:
            self.walls['right'] = False
            other.walls['left'] = False
        elif self.col == other.col and self.row == other.row + 1:
            self.walls['top'] = False
            other.walls['bottom'] = False
        elif self.col == other.col and self.row == other.row - 1:
            self.walls['bottom'] = False
            other.walls['top'] = False

# Cria uma lista de células para representar o labirinto
grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]

# Define a célula inicial do labirinto
current = grid[0][0]

# Cria uma lista de todas as paredes e embaralha aleatoriamente
walls = []
for row in grid:
    for cell in row:
        if cell.col < COLS - 1:
            walls.append((cell, grid[cell.row][cell.col + 1]))
        if cell.row < ROWS - 1:
            walls.append((cell, grid[cell.row + 1][cell.col]))

random.shuffle(walls)

#Variáveis subsets e ranks para a implementação do conjunto de conjuntos de Kruskal
subsets = [i for i in range(ROWS*COLS)]
ranks = [0] * ROWS*COLS

#Implementa o algoritmo de Kruskal para construir o labirinto, removendo paredes entre conjuntos diferentes
for wall in walls:
    cell1, cell2 = wall
    set1 = find(subsets, cell1.row * COLS + cell1.col)
    set2 = find(subsets, cell2.row * COLS + cell2.col)
    if set1 != set2:
        union(subsets, ranks, set1, set2)
        cell1.remove_wall(cell2)


# Loop principal do jogo
running = True
while running:
    # Processa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenha as células do labirinto
    screen.fill(BLACK)
    for row in grid:
        for cell in row:
            cell.draw()

    # Atualiza a tela
    pygame.display.update()
    
    if all(all(cell.visited for cell in row) for row in grid):
        running = False
# Encerra o Pygame
pygame.quit()