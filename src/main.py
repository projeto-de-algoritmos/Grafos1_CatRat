import pygame
pygame.init()

#Configurações do labirinto
fundo = pygame.image.load('maze.png')

#Configurações do rato
x = 0
y = 0
velocidade = 10
rato = pygame.image.load('black-rat.png')

#Configuração da janela do jogo
pygame.display.set_caption("Catch Rat")
janela = pygame.display.set_mode((862,561))
janela_aberta = True

while janela_aberta:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            janela_aberta = False
    
    #Controle de movimentação do rato
    comandos = pygame.key.get_pressed()
    if comandos [pygame.K_UP]:
        y-= velocidade
    if comandos [pygame.K_DOWN]:
        y+= velocidade
    if comandos [pygame.K_RIGHT]:
        x+= velocidade
    if comandos [pygame.K_LEFT]:
        x-= velocidade

    #Desenho de cenário e personagens
    janela.blit(fundo, (0,0))
    janela.blit(rato, (x,y))
    
    pygame.display.update()
pygame.quit()