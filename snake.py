import pygame
import random

window_width = 500
window_height = 500
block_size = 30

pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((window_height, window_width))


white = pygame.Color(255, 255, 255)
black = pygame.Color(0,0,0)
light_green = pygame.Color(144,238,144)

class Snake:
    def __init__(self, block_width):
        self.body = [(0,0), (1,0), (2,0)]
        self.block_width = block_width
        self.direction = 'right'
        self.collision = False
    

    def draw_snake(self, screen):
        x_zero_pix = 10+3.5*30
        y_zero_pix = 10+3.5*30
        for x,y in self.body:
            pygame.draw.rect(screen, white, pygame.rect.Rect(x*self.block_width +x_zero_pix, y*self.block_width + y_zero_pix, block_size, block_size), border_radius=1)

    def set_direction(self, direction):
        if direction == 'up':
            self.direction = 'up'
        elif direction == 'right':
            self.direction = 'right'
        elif direction == 'down':
            self.direction = 'down'
        elif direction == 'left':
            self.direction = 'left'

    def move(self, food_pos=None):
        prev_head = self.body[-1]

        if self.direction == 'up':
            new_head = (prev_head[0], prev_head[1]-1)          
        elif self.direction == 'right':
            new_head = (prev_head[0]+1, prev_head[1])
        elif self.direction == 'down':
            new_head = (prev_head[0], prev_head[1]+1)
        elif self.direction == 'left':
            new_head = (prev_head[0]-1, prev_head[1])
        
        if self.is_collision(new_head[0], new_head[1]):
            self.collision = True
        else:
            self.body.append(new_head)
            if new_head == food_pos: #Eet een nieuw voedsel
                return True
            self.body.pop(0)
            return False
    
    def is_collision(self, x, y):
        if (x,y) in self.body:
            return True
        return False

class Food:
    def __init__(self, block_width, x_zero_pix, y_zero_pix, x_max, y_max):
        self.x = random.randint(0, x_max)
        self.y = random.randint(0, y_max)
        self.x_zero_pix = x_zero_pix
        self.y_zero_pix = y_zero_pix
        self.block_width = block_width

    def draw(self, screen): 
        pygame.draw.rect(screen, light_green, pygame.rect.Rect(self.x*self.block_width + self.x_zero_pix, self.y*self.block_width + self.y_zero_pix, self.block_width, self.block_width))


class Board:
    def __init__(self, x_max, y_max, block_size=30): #The height and widh of the board will have the maximum value such that the blocks * block_size fits precisely. 
        self.x_min = 0
        self.x_max = x_max - 1
        self.y_min = 0
        self.y_max = y_max - 1
        self.zero_pix_x = 0
        self.zero_pix_y = 0
        self.block_size = block_size

    def calculate_margin(self, high_pix, low_pix):
        margin = ((high_pix - low_pix) - ((high_pix - low_pix) // self.block_size)*self.block_size) / 2
        extra_margin = ((high_pix - low_pix) - (self.x_max + 1) * block_size - 2 * margin) / 2
        return margin + extra_margin
    
    def draw(self, screen, top_border, right_border, bottom_border, left_border): #Centralises between these coordinates, if the board is too small and doesn't fit exactly
        margin_height = self.calculate_margin(bottom_border, top_border)
        margin_width = self.calculate_margin(right_border, left_border)
        
        pygame.draw.line(screen, white, (left_border + margin_width, top_border + margin_height), (right_border - margin_width, top_border + margin_height))
        pygame.draw.line(screen, white, (right_border - margin_width, top_border + margin_height), (right_border - margin_width, bottom_border - margin_height))
        pygame.draw.line(screen, white, (right_border - margin_width, bottom_border - margin_height), (left_border + margin_width, bottom_border - margin_height))
        pygame.draw.line(screen, white, (left_border + margin_width, bottom_border - margin_height), (left_border + margin_width, top_border + margin_height))

# Main logic

run = True
board = Board(9, 9)
snake = Snake(block_size)
food = Food(block_size, 10+3.5*30, 10+3.5*30, board.x_max, board.y_max)

ate_food = False


while run:
    new_direction = snake.direction
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != 'down':
                new_direction = 'up'
            elif event.key == pygame.K_RIGHT and snake.direction != 'left':
                new_direction = 'right'
            elif event.key == pygame.K_DOWN and snake.direction != 'up':
                new_direction = 'down'
            elif event.key == pygame.K_LEFT and snake.direction != 'right':
                new_direction = 'left'
    snake.set_direction(new_direction) #Prevents a bug for moving back into yourself.
    ate_food = snake.move((food.x, food.y))

    if ate_food:
        food = Food(block_size,10+3.5*30, 10+3.5*30, board.x_max, board.y_max)
        ate_food = False

    if (board.x_min<= snake.body[-1][0] <=board.x_max and board.y_min <= snake.body[-1][1] <= board.y_max) and not snake.collision:
        game_window.fill(black)
        food.draw(game_window)
        snake.draw_snake(game_window)
    
    else:
        print('botsing')
        run = False
    board.draw(game_window, 0, window_width, window_height, 0)
    pygame.display.update()
    pygame.time.Clock().tick(10)

pygame.quit()
