import pygame
import random

# Ініціалізація Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# Колір фону
back = (255, 255, 255)

# Вікно програми, фонове зображення
mw = pygame.display.set_mode((500, 500))
background = pygame.image.load('fantasy.jpg')  # Файл фону
mw.blit(background, (0, 0))
clock = pygame.time.Clock()

# Швидкість м'яча
dx = random.randint(1, 3)
dy = random.randint(2, 5)

# Початкові координати платформи
platform_x = 200
platform_y = 350

# Прапори руху
move_right = False
move_left = False

# Прапор закінчення гри
game_over = False

# Базовий клас прямокутної області
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        if self.fill_color is not None:
            pygame.draw.rect(mw, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

# Клас для написів
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

# Клас для зображень
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

# Створення об'єктів
ball = Picture('ball3.png', 200, 250, 30, 30)
platform = Picture('platform2.png', platform_x, platform_y, 150, 30)

# Створення ворогів
start_x = 5
start_y = 5
count = 9
monsters = []

for j in range(5):
    y = start_y + (40 * j)
    x = start_x + (27.5 * j)
    for i in range(count):
        d = Picture('enemy4.png', x, y, 35, 35)
        monsters.append(d)
        x += 55
    count -= 1

# Основний цикл гри
while not game_over:
    mw.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False

    # Рух платформи
    if move_right:
        platform.rect.x += 4
    if move_left:
        platform.rect.x -= 4

    # Рух м'яча
    ball.rect.x += dx
    ball.rect.y += dy

    # Відбиття м'яча від країв
    if ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1

    # Умови програшу
    if ball.rect.y > 400:
        pygame.mixer.music.stop()
        game_over = True
        time_text = Label(100, 150, 50, 50)
        time_text.set_text('YOU LOSE', 60, (255, 0, 0))
        time_text.draw(10, 10)
        pygame.display.update() # Оновлення екрану

        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
            pygame.time.delay(50)

    # Умови виграшу
    if len(monsters) == 0:
        pygame.mixer.music.stop()
        game_over = True
        time_text = Label(100, 150, 50, 50)
        time_text.set_text('YOU WIN', 60, (0, 200, 0))
        time_text.draw(10, 10)
        pygame.display.update() # Оновлення екрану

        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
            pygame.time.delay(50)

    # Відбиття м'яча від платформи
    if ball.rect.colliderect(platform.rect):
        dy *= -1

    # Відображення та перевірка монстрів
    for m in monsters:
        m.draw()
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            dy *= -1

    platform.draw()
    ball.draw()

    pygame.display.update()
    clock.tick(40)
