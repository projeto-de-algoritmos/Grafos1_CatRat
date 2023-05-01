import pygame
from map import mapa
import sys

# Define as dimensões da janela
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Define as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (136, 8, 8)

# Define a velocidade do personagem
CHARACTER_SPEED = 20

# Inicializa o Pygame
pygame.init()

# Cria a janela do jogo
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Cria o objeto do personagem
character = pygame.Rect(00, 160, 20, 20)

# Cria o objeto do inimigo
enemy = pygame.Rect(380, 360, 20, 20)

# Criando o grafo
graph = {}
for row in range(len(mapa)):
    for col in range(len(mapa[row])):
        if mapa[row][col] == ".":
            neighbors = []
            if row > 0 and mapa[row-1][col] == ".":
                neighbors.append((row-1, col))
            if row < len(mapa)-1 and mapa[row+1][col] == ".":
                neighbors.append((row+1, col))
            if col > 0 and mapa[row][col-1] == ".":
                neighbors.append((row, col-1))
            if col < len(mapa[row])-1 and mapa[row][col+1] == ".":
                neighbors.append((row, col+1))
            graph[(row, col)] = neighbors

def draw_graph(graph):
    for node, neighbors in graph.items():
        # Desenha um quadrado para representar o nó
        pygame.draw.rect(screen, WHITE, (node[1]*20, node[0]*20, 20, 20))
        # Desenha uma linha para cada vizinho do nó
        for neighbor in neighbors:
            pygame.draw.line(screen, WHITE, (node[1]*20+10, node[0]*20+10), (neighbor[1]*20+10, neighbor[0]*20+10))



# Loop principal do jogo
while True:
    # Desenha o mapa do labirinto na tela
    draw_graph(graph)

    # Desenha o personagem na tela
    pygame.draw.rect(screen, BLUE, character)
    
    # Desenha o inimigo na tela
    pygame.draw.rect(screen, RED, enemy)

    # Atualiza a tela
    pygame.display.update()

    # Define o nó atual do personagem
    current_node = (character.y // 20, character.x // 20)
    
    # Espera por eventos do usuário
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Verifica se uma tecla foi pressionada
        elif event.type == pygame.KEYDOWN:
            # Verifica a direção da tecla pressionada
            if event.key == pygame.K_UP:
                next_node = (current_node[0] - 1, current_node[1])
                if next_node in graph[current_node]:
                    character.move_ip(0, -CHARACTER_SPEED)
                    current_node = next_node
            elif event.key == pygame.K_DOWN:
                next_node = (current_node[0] + 1, current_node[1])
                if next_node in graph[current_node]:
                    character.move_ip(0, CHARACTER_SPEED)
                    current_node = next_node
            elif event.key == pygame.K_LEFT:
                next_node = (current_node[0], current_node[1] - 1)
                if next_node in graph[current_node]:
                    character.move_ip(-CHARACTER_SPEED, 0)
                    current_node = next_node
            elif event.key == pygame.K_RIGHT:
                next_node = (current_node[0], current_node[1] + 1)
                if next_node in graph[current_node]:
                    character.move_ip(CHARACTER_SPEED, 0)
                    current_node = next_node

            # Atualiza a posição do inimigo em relação à posição atual do jogador
            if character.x < enemy.x:
                enemy.move_ip(-CHARACTER_SPEED, 0)
            elif character.x > enemy.x:
                enemy.move_ip(CHARACTER_SPEED, 0)
            if character.y < enemy.y:
                enemy.move_ip(0, -CHARACTER_SPEED)
            elif character.y > enemy.y:
                enemy.move_ip(0, CHARACTER_SPEED)
