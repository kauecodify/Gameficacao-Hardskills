import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 30
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
OBSTACLE_SPEED = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, GREEN, [(0, 0), (PLAYER_WIDTH / 2, PLAYER_HEIGHT), (PLAYER_WIDTH, 0)])
        pygame.draw.rect(self.image, GREEN, (0, PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT * 2))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Garantir que o jogador não saia da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        self.rect.y = random.randrange(-100, -OBSTACLE_HEIGHT)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
            self.rect.y = random.randrange(-100, -OBSTACLE_HEIGHT)
            self.speedy = random.randrange(1, 4)

soft_skills_list = ["Comunicação", "Trabalho em Equipe", "Criatividade"]

motivational_quote = "Os obstáculos não devem te impedir, eles devem te fortalecer!"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Evite os Obstáculos!')

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(8):
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

clock = pygame.time.Clock()
game_started = False
start_time = None
score = 0
congrats_time = None
show_congrats = False

# Definindo a função para o botão iniciar
def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    font = pygame.font.SysFont(None, 30)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + (w / 2), y + (h / 2)))
    screen.blit(text_surf, text_rect)

def start_game():
    global game_started, start_time, score
    game_started = True
    start_time = pygame.time.get_ticks()  # Armazenar o tempo de início
    score = 0
    for obstacle in obstacles:
        obstacle.rect.x = random.randrange(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        obstacle.rect.y = random.randrange(-100, -OBSTACLE_HEIGHT)

def restart_game():
    global game_started, start_time, score
    game_started = False
    start_time = None
    score = 0
    for obstacle in obstacles:
        obstacle.rect.x = random.randrange(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        obstacle.rect.y = random.randrange(-100, -OBSTACLE_HEIGHT)

# Função para exibir todas as soft skills
def show_all_soft_skills():
    font = pygame.font.SysFont(None, 24)
    text_y = 60
    for skill in soft_skills_list:
        text = font.render(f"Soft Skill: {skill}", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, text_y))
        text_y += 30

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Renderização
    screen.fill(BLACK)
    if not game_started:
        # Exibir frase motivacional sobre obstáculos
        font = pygame.font.SysFont(None, 24)
        text = font.render(motivational_quote, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 100))

        show_all_soft_skills()

        draw_button("Iniciar", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50, GREEN, (0, 255, 0), start_game)
    else:
        all_sprites.update()

        # Verificando colisões
        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            print("Game Over!")
            restart_game()

        current_time = pygame.time.get_ticks()
        score = (current_time - start_time) // 1000  # Pontuação em segundos

        if score in [10, 20, 30]:
            font = pygame.font.SysFont(None, 24)
            text = font.render(f"Soft Skill: {soft_skills_list[score // 10 - 1]}", True, WHITE)
            screen.blit(text, (10, 30))
            
        if score == 40 and not show_congrats:
            congrats_time = pygame.time.get_ticks()
            show_congrats = True
            
        if show_congrats:
            font = pygame.font.SysFont(None, 36)
            text = font.render("Parabéns, você sabe as principais soft skills!", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            show_all_soft_skills()  # Exibir todas as soft skills
            
            if pygame.time.get_ticks() - congrats_time > 10000:  # Exibir por 10 segundos
                show_congrats = False
                restart_game()

        all_sprites.draw(screen)
        
        # Calcular e exibir o tempo decorrido
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Tempo: {score}", True, WHITE)
        screen.blit(text, (10, 10))

    pygame.display.flip()
