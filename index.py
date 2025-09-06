import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT
# inicializar

pygame.init()
tamanho_tela=(600, 500)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick block")


tamanho_bola= 15
bola= pygame.Rect(100,200, tamanho_bola, tamanho_bola)
tamanho_jogador= 100
jogador=pygame.Rect(250,470, tamanho_jogador, 15 )
qtd_blocos_linha= 8
qtd_linha_bloco= 5
qtd_total_blocos= qtd_blocos_linha * qtd_linha_bloco


def criar_blocos(qtd_blocos_linha, qtd_linha_bloco):
    altura= tamanho_tela[1]
    largura= tamanho_tela[0]
    blocos= []
    distancia_entre_blocos= 5
 
    largura_bloco= largura // qtd_blocos_linha - distancia_entre_blocos
    altura_bloco= 15
    distancia_entre_linhas= altura_bloco + 10
    blocos= []
    
    for j in range(qtd_linha_bloco):
        for i in range(qtd_blocos_linha):
            #criar o bloco
            bloco= pygame.Rect(i*(largura_bloco+distancia_entre_blocos),j * distancia_entre_linhas, largura_bloco, altura_bloco)
            blocos.append(bloco)
    return blocos


cores= {
    "branco": (255, 255, 255),
    "preto": (0, 0, 0),
    "amarelo": (255, 255, 0),
    "azul": (0, 0, 255),
    "verde": (0, 255, 0),
}


fim_jogo= False
game_over= False
pontuacao= 0
movimento_bola= [1, -1]
fonte = pygame.font.Font(None, 74) 


#desenhar a tela
def desenhar_tela():
    tela.fill(cores["preto"])
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela,cores["branco"],bola)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)


#CLAUDE, revisar par
def mostrar_game_over():
    texto = fonte.render("VOCE PERDEU", True, cores["branco"])
    texto_rect = texto.get_rect(center=(tamanho_tela[0]//2, tamanho_tela[1]//2))
    tela.blit(texto, texto_rect)
    
    texto_restart = pygame.font.Font(None, 36).render("Pressione SPACE para jogar novamente", True, cores["amarelo"])
    restart_rect = texto_restart.get_rect(center=(tamanho_tela[0]//2, tamanho_tela[1]//2 + 80))
    tela.blit(texto_restart, restart_rect)


#FUNCOES DO JOGO

def movimentar_jogador():
    teclas = pygame.key.get_pressed()
    velocidade = 3  # Velocidade de movimento
    
    if teclas[pygame.K_RIGHT]:
        if (jogador.x + tamanho_jogador) < tamanho_tela[0]:
            jogador.x += velocidade
    
    if teclas[pygame.K_LEFT]:
        if jogador.x > 0:
            jogador.x -= velocidade
            

def movimentar_bola(bola):
    movimento = movimento_bola.copy()
    bola.x += movimento[0]
    bola.y += movimento[1]
    
    if bola.x <=0:
        movimento[0]= -movimento[0]
    if bola.y <=0:
        movimento[1]= -movimento[1]
    
    if bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0]= -movimento[0]
    if bola.y + tamanho_bola >= tamanho_tela[1]:
        return None  
        
    if jogador.colliderect(bola):
        movimento[1]= -movimento[1]    
    
    for bloco in blocos:
        if bloco.colliderect(bola):
            movimento[1]= -movimento[1]
            blocos.remove(bloco)
            break             
    
    return movimento
                



blocos= criar_blocos(qtd_blocos_linha, qtd_linha_bloco)

#loop infinito
while not fim_jogo:
    desenhar_tela()
    desenhar_blocos(blocos)
    
    if game_over:
        mostrar_game_over()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_jogo= True
        
        if game_over and evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            # Reiniciar o jogo
            game_over = False
            bola.x = 100
            bola.y = 200
            movimento_bola = [1, -1]
            blocos = criar_blocos(qtd_blocos_linha, qtd_linha_bloco)
            
    
    if not game_over:
        movimentar_jogador()        
    
    if not game_over:
        movimento_bola=movimentar_bola(bola)      
        if not movimento_bola:
            game_over=True    
    pygame.time.wait(2)
    pygame.display.flip()
pygame.quit()    
        #fmmfpomfo
        