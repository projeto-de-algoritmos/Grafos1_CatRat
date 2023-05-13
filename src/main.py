import pygame
from map import mapa
import sys
from collections import deque
from collections import defaultdict
from heapq import *
from unionfind import UnionFind

# Define as dimensões da janela
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

#declarações das imagens
GameOver = pygame.image.load('pictures/GameOver.jpg')
YouWin = pygame.image.load('pictures/Sucesso.jpg')

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
pygame.display.set_caption("Catch Rat")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Cria o objeto do personagem
character = pygame.Rect(00, 160, 20, 20)

# Cria o objeto do inimigo
enemy = pygame.Rect(380, 360, 20, 20)

# Cria o objeto do troféu
trophy = pygame.Rect(380, 220, 20, 20)

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

# Função que implementa o algoritmo de Kruskal
def kruskal(self, start, end):
    # Inicializa a lista de arestas e o conjunto de vértices
    edges = [(w, u, v) for u in self.graph for v, w in self.graph[u].items()]
    vertices = set(self.graph.keys())

    # Inicializa a estrutura de Union-Find
    uf = UnionFind(vertices)

    # Ordena as arestas pelo peso (menor para o maior)
    edges.sort()

    # Adiciona as arestas uma a uma até que o caminho seja encontrado
    for weight, u, v in edges:
        if uf[u] != uf[v]:
            uf.union(u, v)
            self.path[u].append(v)
            self.path[v].append(u)
        if uf[start] == uf[end]:
            break

def find_shortest_path(self, start, end):
    # Inicializa o caminho mais curto
    self.path = defaultdict(list)

    # Chama o algoritmo de Kruskal para encontrar o caminho mais curto
    self.kruskal(start, end)

    # Inicializa a lista de vértices visitados e adiciona o nó inicial
    visited = set()
    visited.add(start)

    # Inicializa a fila de nós a serem visitados e adiciona o nó inicial
    queue = [(start, [])]

    # Enquanto houver nós na fila
    while queue:
        # Remove o primeiro nó da fila
        node, path = queue.pop(0)

        # Verifica se o nó é o nó final
        if node == end:
            return path + [node]

        # Adiciona os vizinhos do nó à fila
        for neighbor in self.path[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [node]))

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
        screen.blit(YouWin, (0,0))
        pygame.display.update()
        pygame.time.wait(2500)
        pygame.quit()
        sys.exit()

    # Define o nó atual do inimigo
    enemy_node = (enemy.y // 20, enemy.x // 20)

    # Define o nó inicial e o nó objetivo para o inimigo
    enemy_start = (enemy.y // 20, enemy.x // 20)
    enemy_goal = (character.y // 20, character.x // 20)
    
    # Chama a função find_shortest_path para encontrar o caminho até o objetivo
    enemy_path = find_shortest_path(graph, enemy_start, enemy_goal)

    #Condição de derrota
    if (enemy.y // 20, enemy.x // 20) == (character.y // 20, character.x // 20):
        print("Você perdeu!")
        screen.blit(GameOver, (0,0))
        pygame.display.update()
        pygame.time.wait(2500)
        pygame.quit()
        sys.exit()

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
    path = find_shortest_path(graph, enemy_node, (character.y // 20, character.x // 20))

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

    pygame.time.wait(250)

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
    
    pygame.display.update()
