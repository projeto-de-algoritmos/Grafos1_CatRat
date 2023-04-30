import pygame
pygame.init()
x = 300
y = 400
velocidade = 10
fundo = pygame.image.load('maze.png')
rato = pygame.image.load('black-rat.png')

janela = pygame.display.set_mode((862,561))
pygame.display.set_caption("Criando um jogo com python")

janela_aberta = True
while janela_aberta:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            janela_aberta = False

    comandos = pygame.key.get_pressed()
    if comandos [pygame.K_UP]:
        y-= velocidade
    if comandos [pygame.K_DOWN]:
        y+= velocidade
    if comandos [pygame.K_RIGHT]:
        x+= velocidade
    if comandos [pygame.K_LEFT]:
        x-= velocidade

    janela.blit(fundo, (0,0))
    janela.blit(rato, (x,y))
    
    pygame.display.update()
pygame.quit()