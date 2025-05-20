import pgzrun
import random

# Configurações
WIDTH = 800
HEIGHT = 600
TITLE = "Super Mario Simplificado"
GRAVITY = 0.8
JUMP_STRENGTH = -18
PLAYER_SPEED = 5
ENEMY_SPEED = 2

# Estados do jogo
MENU = 0
PLAYING = 1
GAME_OVER = 2
VICTORY = 3
game_state = MENU

# Tamanhos
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 20
COIN_SIZE = 20
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 40

class Player:
    def __init__(self):
        self.rect = Rect((100, 300), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.vy = 0
        self.on_ground = False
        self.facing_right = True
        self.score = 0
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0

    def update(self, platforms, coins, enemies):
        global game_state
        
        if game_state != PLAYING:
            return
            
        # Movimento
        move_x = 0
        if keyboard.left:
            move_x -= PLAYER_SPEED
            self.facing_right = False
        if keyboard.right:
            move_x += PLAYER_SPEED
            self.facing_right = True
        
        self.rect.x += move_x
        
        # Gravidade
        self.vy += GRAVITY
        self.rect.y += self.vy
        
        # Colisão com plataformas
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vy > 0:
                self.rect.bottom = platform.rect.top
                self.vy = 0
                self.on_ground = True
        
        # Coletar moedas
        for coin in coins:
            if not coin.collected and self.rect.colliderect(coin.rect):
                coin.collected = True
                self.score += 1
        
        # Colisão com inimigos
        if not self.invincible:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    self.lives -= 1
                    self.invincible = True
                    self.invincible_timer = 60
                    self.rect.x -= 50
                    if self.lives <= 0:
                        game_state = GAME_OVER
                    break
        
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        if self.rect.top > HEIGHT:
            self.lives -= 1
            self.reset_position()
            if self.lives <= 0:
                game_state = GAME_OVER

    def reset_position(self):
        self.rect.x = 100
        self.rect.y = 300
        self.vy = 0

    def draw(self):
        if not self.invincible or self.invincible_timer % 10 < 5:
            color = (255, 0, 0) if not self.invincible else (255, 255, 255)
            screen.draw.filled_rect(self.rect, color)
            
            eye_y = self.rect.y + 15
            if self.facing_right:
                screen.draw.filled_circle((self.rect.right - 15, eye_y), 5, (255, 255, 255))
                screen.draw.filled_circle((self.rect.right - 10, eye_y), 3, (0, 0, 0))
            else:
                screen.draw.filled_circle((self.rect.left + 15, eye_y), 5, (255, 255, 255))
                screen.draw.filled_circle((self.rect.left + 10, eye_y), 3, (0, 0, 0))

class Platform:
    def __init__(self, x, y, width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT):
        self.rect = Rect((x, y), (width, height))
    
    def draw(self):
        screen.draw.filled_rect(self.rect, (34, 139, 34))
        screen.draw.line((self.rect.left, self.rect.top + 5), 
                        (self.rect.right, self.rect.top + 5), (0, 100, 0))

class Coin:
    def __init__(self, x, y):
        self.rect = Rect((x, y), (COIN_SIZE, COIN_SIZE))
        self.collected = False
        self.animation_frame = 0
    
    def draw(self):
        if not self.collected:
            size = COIN_SIZE//2 + int(2 * abs((self.animation_frame % 10) - 5))
            screen.draw.filled_circle(self.rect.center, size, (255, 215, 0))
            screen.draw.circle(self.rect.center, size, (255, 165, 0))
            self.animation_frame += 0.5

class Enemy:
    def __init__(self, x, y):
        self.rect = Rect((x, y), (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.direction = 1
        self.speed = ENEMY_SPEED
        self.animation_frame = 0
    
    def update(self, platforms):
        self.rect.x += self.direction * self.speed
        
        on_platform = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and abs(self.rect.bottom - platform.rect.top) < 5:
                on_platform = True
                if (self.direction > 0 and self.rect.right > platform.rect.right) or (self.direction < 0 and self.rect.left < platform.rect.left):
                    self.direction *= -1
                break
        
        if not on_platform:
            self.direction *= -1
            self.rect.y += 5
    
    def draw(self):
        screen.draw.filled_rect(self.rect, (128, 0, 128))
        
        eye_offset = int(3 * (self.animation_frame % 5))
        left_eye_x = self.rect.left + 15 + (self.direction * eye_offset)
        right_eye_x = self.rect.right - 15 + (self.direction * eye_offset)
        
        screen.draw.filled_circle((left_eye_x, self.rect.top + 15), 5, (255, 255, 255))
        screen.draw.filled_circle((right_eye_x, self.rect.top + 15), 5, (255, 255, 255))
        screen.draw.filled_circle((left_eye_x + 2, self.rect.top + 15), 3, (0, 0, 0))
        screen.draw.filled_circle((right_eye_x + 2, self.rect.top + 15), 3, (0, 0, 0))
        
        self.animation_frame += 0.2

class Button:
    def __init__(self, x, y, text, color=(70, 130, 180)):
        self.rect = Rect((x, y), (200, 50))
        self.text = text
        self.color = color
    
    def draw(self):
        screen.draw.filled_rect(self.rect, self.color)
        screen.draw.rect(self.rect, (255, 255, 255))
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=30,
            color=(255, 255, 255)
        )
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Inicialização
player = Player()
platforms = []
coins = []
enemies = []

# Botões do menu
start_button = Button(WIDTH//2 - 100, HEIGHT//2, "Iniciar Jogo")
quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, "Sair", (255, 0, 0))
restart_button = Button(WIDTH//2 - 100, HEIGHT//2, "Reiniciar")

def create_world():
    global platforms, coins, enemies
    
    platforms = [
        Platform(0, 570, WIDTH, 30),
        Platform(200, 450),
        Platform(400, 450),
        Platform(300, 350),
        Platform(500, 350),
        Platform(200, 250),
        Platform(400, 250),
        Platform(600, 250)
    ]
    
    coins = []
    for _ in range(15):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(100, HEIGHT - 100)
        coins.append(Coin(x, y))
    
    enemies = [
        Enemy(300, 400),
        Enemy(500, 400),
        Enemy(200, 200)
    ]

def start_game():
    global game_state, player
    game_state = PLAYING
    player = Player()
    create_world()

def draw():
    screen.fill((135, 206, 235))
    
    # Nuvens de fundo
    for i in range(3):
        screen.draw.filled_circle((100 + i*300, 100), 30, (255, 255, 255))
        screen.draw.filled_circle((130 + i*300, 100), 40, (255, 255, 255))
        screen.draw.filled_circle((160 + i*300, 100), 30, (255, 255, 255))
    
    if game_state == MENU:
        screen.draw.text(
            "SUPER MARIO PYTHON",
            center=(WIDTH//2, HEIGHT//4),
            fontsize=60,
            color=(255, 0, 0),
            shadow=(2, 2),
            scolor="black"
        )
        start_button.draw()
        quit_button.draw()
    
    elif game_state == PLAYING:
        for platform in platforms:
            platform.draw()
        
        for coin in coins:
            coin.draw()
        
        for enemy in enemies:
            enemy.draw()
        
        player.draw()
        
        screen.draw.text(
            f"Moedas: {player.score}",
            topleft=(15, 15),
            fontsize=30,
            color=(0, 0, 0),
            background=(255, 255, 255)
        )
        screen.draw.text(
            f"Vidas: {player.lives}",
            topleft=(15, 50),
            fontsize=30,
            color=(0, 0, 0),
            background=(255, 255, 255)
        )
    
    elif game_state == GAME_OVER:
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH//2, HEIGHT//3),
            fontsize=60,
            color=(255, 0, 0),
            shadow=(2, 2),
            scolor="black"
        )
        screen.draw.text(
            f"Pontuação: {player.score}",
            center=(WIDTH//2, HEIGHT//2 - 30),
            fontsize=40,
            color=(0, 0, 0))
        restart_button.draw()
        quit_button.draw()
    
    elif game_state == VICTORY:
        screen.draw.text(
            "VOCÊ VENCEU!",
            center=(WIDTH//2, HEIGHT//3),
            fontsize=60,
            color=(255, 215, 0),
            shadow=(2, 2),
            scolor="black"
        )
        screen.draw.text(
            f"Pontuação Final: {player.score}",
            center=(WIDTH//2, HEIGHT//2 - 30),
            fontsize=40,
            color=(0, 0, 0))
        restart_button.draw()
        quit_button.draw()

def update():
    global game_state
    
    if game_state == PLAYING:
        player.update(platforms, coins, enemies)
        
        for enemy in enemies:
            enemy.update(platforms)
        
        if all(coin.collected for coin in coins):
            game_state = VICTORY

def on_mouse_down(pos):
    if game_state == MENU:
        if start_button.is_clicked(pos):
            start_game()
        elif quit_button.is_clicked(pos):
            quit()
    
    elif game_state in (GAME_OVER, VICTORY):
        if restart_button.is_clicked(pos):
            start_game()
        elif quit_button.is_clicked(pos):
            quit()

def on_key_down(key):
    global game_state
    
    if game_state == PLAYING:
        if key == keys.SPACE and player.on_ground:
            player.vy = JUMP_STRENGTH
        elif key == keys.ESCAPE:
            game_state = MENU

pgzrun.go()