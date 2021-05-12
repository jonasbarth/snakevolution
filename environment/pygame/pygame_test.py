import pygame

width = 400
height = 400
snake_size = 20

pygame.init()
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
window = pygame.display.set_mode((width, height))

# 0,0 is in the top left corner
#
center_x = width / 2 - snake_size / 2
center_y = height / 2 - snake_size / 2
snake = pygame.Rect(center_x, center_y, snake_size, snake_size)
pygame.draw.rect(window, red, snake)
pygame.display.flip()
running = True
direction = 'RIGHT'
change_to = direction
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    elif event.type == pygame.KEYDOWN:
        # W -> Up; S -> Down; A -> Left; D -> Right
        if event.key == pygame.K_UP or event.key == ord('w'):
            change_to = 'UP'
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            change_to = 'DOWN'
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            change_to = 'LEFT'
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            change_to = 'RIGHT'
        # Esc -> Create event to quit the game
        if event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake.move_ip(0, -snake_size)
        if direction == 'DOWN':
            snake.move_ip(0, snake_size)
        if direction == 'LEFT':
            snake.move_ip(-snake_size, 0)
        if direction == 'RIGHT':
            snake.move_ip(snake_size, 0)

        window.fill(black)
        pygame.draw.rect(window, red, snake)
        pygame.display.flip()