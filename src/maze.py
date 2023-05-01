import sys
import networkx as nx
import pygame
import random

# Tamanho do labirinto
MAZE_SIZE = 50

# Criando um grafo MAZE_SIZE x MAZE_SIZE
maze = nx.grid_2d_graph(MAZE_SIZE, MAZE_SIZE)

# Adicionando paredes aleatórias
for node in list(maze.nodes()):
    if random.random() < 0.3:
        maze.remove_node(node)

# Criando uma matriz 2D do labirinto
maze_array = [[1 if maze.has_node((row, col)) else 0 for col in range(MAZE_SIZE)] for row in range(MAZE_SIZE)]

def draw_maze():
    for row in range(len(maze_array)):
        for col in range(len(maze_array[row])):
            cell = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze_array[row][col] == 1:
                pygame.draw.rect(screen, WALL_COLOR, cell)
            else:
                pygame.draw.rect(screen, CELL_COLOR, cell)

import networkx as nx
import pygame
import random

# Tamanho do labirinto
MAZE_SIZE = 50

# Criando um grafo MAZE_SIZE x MAZE_SIZE
maze = nx.grid_2d_graph(MAZE_SIZE, MAZE_SIZE)

# Adicionando paredes aleatórias
for node in list(maze.nodes()):
    if random.random() < 0.3:
        maze.remove_node(node)

# Criando uma matriz 2D do labirinto
maze_array = [[1 if maze.has_node((row, col)) else 0 for col in range(MAZE_SIZE)] for row in range(MAZE_SIZE)]

# Configurações da janela
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20

# Cores
CELL_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
PLAYER_COLOR = (255, 0, 0)

# Inicializando o Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Configurando a posição inicial do jogador
player_row = 0
player_col = 0

# Loop principal do jogo
while True:
    # Processando eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and maze_array[player_row-1][player_col] == 0:
                player_row -= 1
            elif event.key == pygame.K_DOWN and maze_array[player_row+1][player_col] == 0:
                player_row += 1
            elif event.key == pygame.K_LEFT and maze_array[player_row][player_col-1] == 0:
                player_col -= 1
            elif event.key == pygame.K_RIGHT and maze_array[player_row][player_col+1] == 0:
                player_col += 1

    # Limpando a tela
    screen.fill((255, 255, 255))

    #Desenhando o labirinto
    draw_maze()

    # Desenhando o jogador
    player_rect = pygame.Rect(player_col*CELL_SIZE, player_row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Atualizando a tela
    pygame.display.flip()

    # Limitando a taxa de quadros
    clock.tick(60)
