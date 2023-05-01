import pygame
from map import mapa
import sys
from collections import deque

# Define as dimensões da janela
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Define as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (136, 8, 8)
YELLOW = (212,175,55)

# Define a velocidade dos personagens
CHARACTER_SPEED = 20
ENEMY_SPEED = 10

# Inicializa o Pygame
pygame.init()

# Cria a janela do jogo
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Cria o objeto do personagem
character = pygame.Rect(00, 160, 20, 20)

# Cria o objeto do inimigo
enemy = pygame.Rect(380, 360, 20, 20)

# Cria o objeto do troféu
trophy = pygame.Rect(20, 160, 20, 20)
#380, 220

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

# Função que implementa o algoritmo BFS
def bfs(graph, start, goal):
    # Inicializa a fila com o nó inicial
    queue = [start]
    # Inicializa o dicionário de predecessores
    predecessor = {start: None}
    
    # Loop principal do algoritmo BFS
    while queue:
        # Remove o nó mais antigo da fila
        current_node = queue.pop(0)
        
        # Verifica se o nó atual é o objetivo
        if current_node == goal:
            # Se for, monta o caminho e retorna
            path = [current_node]
            while predecessor[current_node]:
                current_node = predecessor[current_node]
                path.append(current_node)
            return path[::-1]
        
        # Adiciona os vizinhos não visitados do nó atual na fila
        for neighbor in graph[current_node]:
            if neighbor not in predecessor:
                predecessor[neighbor] = current_node
                queue.append(neighbor)
    
    # Se o objetivo não foi encontrado, retorna None
    return None

# Define o nó objetivo para o inimigo
enemy_goal = (character.y // 20, character.x // 20)

# Loop principal do jogo
while True:
    # Desenha o mapa do labirinto na tela
    draw_graph(graph)

    # Define o nó atual do troféu
    trophy_node = (trophy.y // 20, trophy.x // 20)
    
    # Desenha o troféu na tela
    pygame.draw.rect(screen, YELLOW, trophy)
    
    #Condição de vitória
    if (character.y // 20, character.x // 20) == (trophy.y // 20, trophy.x // 20):
        print("Você venceu!")
        pygame.time.wait(5000)

    # Define o nó atual do inimigo
    enemy_node = (enemy.y // 20, enemy.x // 20)

    # Define o nó inicial e o nó objetivo para o inimigo
    enemy_start = (enemy.y // 20, enemy.x // 20)
    enemy_goal = (character.y // 20, character.x // 20)
    
    # Chama a função bfs para encontrar o caminho até o objetivo
    enemy_path = bfs(graph, enemy_start, enemy_goal)

    #Condição de derrota
    if (enemy.y // 20, enemy.x // 20) == (character.y // 20, character.x // 20):
        print("Você perdeu!")
        pygame.time.wait(5000)


    # Se o caminho foi encontrado, atualiza a posição do inimigo
    if len(enemy_path) >= 2:
        next_node = enemy_path[1]
    else:
        next_node = None

    if next_node:
        if next_node[0] < enemy_start[0]:
            enemy.move_ip(0, -CHARACTER_SPEED)
        elif next_node[0] > enemy_start[0]:
            enemy.move_ip(0, CHARACTER_SPEED)
        elif next_node[1] < enemy_start[1]:
            enemy.move_ip(-CHARACTER_SPEED, 0)
        elif next_node[1] > enemy_start[1]:
            enemy.move_ip(CHARACTER_SPEED, 0)
        enemy_start = next_node

    # Encontra o caminho mais curto do inimigo até o personagem
    path = bfs(graph, enemy_node, (character.y // 20, character.x // 20))

    # Move o inimigo em direção ao próximo nó do caminho
    if path:
        next_node = path[0]
        if next_node[1] < enemy_node[1]:
            enemy.move_ip(-ENEMY_SPEED, 0)
        elif next_node[1] > enemy_node[1]:
            enemy.move_ip(ENEMY_SPEED, 0)
        elif next_node[0] < enemy_node[0]:
            enemy.move_ip(0, -ENEMY_SPEED)
        elif next_node[0] > enemy_node[0]:
            enemy.move_ip(0, ENEMY_SPEED)
        enemy_node = (enemy.y // 20, enemy.x // 20)

    pygame.time.wait(500)

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
