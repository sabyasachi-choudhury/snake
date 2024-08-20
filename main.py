import pygame
from pygame.locals import *
import random

pygame.init()

# Vars
run = True
s_len = 800
block_len = 40
rows = int(s_len / block_len)
turns = []
turning = False
points = 0
new_center = [0, 0]
added = False

# Screen
screen = pygame.display.set_mode((s_len, s_len))


# Block class
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Block, self).__init__()
        self.surf = pygame.Surface((block_len - 1, block_len - 1))
        self.surf.fill((57, 255, 20))
        self.x, self.y = block_len * (x - 1) + block_len / 2, block_len * (y - 1) + block_len / 2,
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.x_dir, self.y_dir = 1, 0


# Apple class
class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super(Apple, self).__init__()
        self.surf = pygame.Surface((block_len - 1, block_len - 1))
        self.surf.fill((255, 38, 38))
        self.rect = self.surf.get_rect(center=(random.choice(range(int(block_len / 2), s_len, block_len)),
                                               random.choice(range(int(block_len / 2), s_len, block_len))))


def snake_motion():
    global run, turns
    index = 0
    # Basic motions
    for part in snake:
        index += 1
        part.rect.move_ip(block_len * part.x_dir, block_len * part.y_dir)
        # Using turn points
        for details in turns:
            if part.rect.center == details[0]:
                part.x_dir = details[1]
                part.y_dir = details[2]
                if index == len(snake):
                    turns.remove(details)

    # Self crash
    crash_group = pygame.sprite.Group()
    for x in snake:
        if x != head:
            crash_group.add(x)
    for c_block in crash_group:
        if pygame.sprite.collide_rect(head, c_block):
            run = False
    # Wall crash
    if head.rect.centerx < 0 or head.rect.centerx > s_len or head.rect.centery < 0 or head.rect.centery > s_len:
        run = False


def snake_turn():
    global turns, turning
    if event.key == K_UP and head.y_dir == 0 and not turning:
        head.x_dir, head.y_dir = 0, -1
        turns.append([head.rect.center, 0, -1])
        turning = True
    elif event.key == K_DOWN and head.y_dir == 0 and not turning:
        head.x_dir, head.y_dir = 0, 1
        turns.append([head.rect.center, 0, 1])
        turning = True
    elif event.key == K_LEFT and head.x_dir == 0 and not turning:
        head.x_dir, head.y_dir = -1, 0
        turns.append([head.rect.center, -1, 0])
        turning = True
    elif event.key == K_RIGHT and head.x_dir == 0 and not turning:
        head.x_dir, head.y_dir = 1, 0
        turns.append([head.rect.center, 1, 0])
        turning = True


# Objects and groups
head = Block(10, 10)
start_tail = Block(9, 10)
snake = pygame.sprite.Group(head, start_tail)
apples = pygame.sprite.Group(Apple())
tail = pygame.sprite.Group(start_tail)

# Mainloop
while run:
    # Fill
    screen.fill((0, 0, 0))

    # Reset var
    turning = False

    # Event detection
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
            snake_turn()

    # Add apple
    if len(apples) == 0:
        apples.add(Apple())

    # Apple eating
    for f in apples:
        if pygame.sprite.spritecollideany(f, snake):
            f.kill()
            points += 1
            snake.add(Block(s_len/2, s_len/2))
            for t in tail:
                a = Block(int(t.rect.centerx/block_len + 0.5), int(t.rect.centery/block_len + 0.5))
                a.x_dir, a.y_dir = t.x_dir, t.y_dir
                tail = pygame.sprite.Group(a)
                added = True

    # Snake motion
    snake_motion()

    if added:
        snake.add(a)
        added = False

    # Blit
    for fruit in apples:
        screen.blit(fruit.surf, fruit.rect)
    for block in snake:
        screen.blit(block.surf, block.rect)

    # Grid
    for x in range(rows):
        pygame.draw.line(screen, (255, 255, 255), (0, x * block_len), (s_len, x * block_len))
        pygame.draw.line(screen, (255, 255, 255), (x * block_len, 0), (x * block_len, s_len))

    # Flip and frame rate
    pygame.display.flip()
    pygame.time.Clock().tick(10)

pygame.quit()
print(points)