import pgzrun
import random

# Configurações básicas
WIDTH = 800
HEIGHT = 600
TITLE = "Coletor de Moedas"

# Cria o jogador (usando um retângulo se não tiver imagem)
player = Actor('player', (400, 300))
player.speed = 5

# Lista de moedas
coins = []
score = 0

def draw_actor(actor, color=(255, 255, 0)):
    """Desenha um ator como círculo se a imagem não existir"""
    if hasattr(actor, 'image') and actor.image:
        actor.draw()
    else:
        screen.draw.filled_circle((actor.x, actor.y), 20, color)

def create_coin():
    """Cria uma nova moeda"""
    coin = Actor('coin', (random.randint(50, WIDTH-50), 
                        random.randint(50, HEIGHT-50)))
    coins.append(coin)

def update():
    global score
    
    # Controles simplificados
    if keyboard.left: player.x -= player.speed
    if keyboard.right: player.x += player.speed
    if keyboard.up: player.y -= player.speed
    if keyboard.down: player.y += player.speed
    
    # Verifica colisões
    for coin in coins[:]:
        if abs(player.x - coin.x) < 30 and abs(player.y - coin.y) < 30:
            coins.remove(coin)
            score += 1
            create_coin()

def draw():
    screen.fill((80, 150, 220))
    
    # Desenha todas as moedas
    for coin in coins:
        draw_actor(coin, (255, 215, 0))  # Cor dourada
    
    # Desenha o jogador
    draw_actor(player, (255, 0, 0))  # Cor vermelha
    
    # Mostra o placar
    screen.draw.text(f"Pontos: {score}", (20, 20), fontsize=50, color="white")

# Cria moedas iniciais
for _ in range(5):
    create_coin()

pgzrun.go()