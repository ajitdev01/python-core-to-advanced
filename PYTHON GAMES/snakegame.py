import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors - Modern color palette
DARK_BG = (20, 20, 30)
LIGHT_BG = (30, 30, 45)
SNAKE_COLOR = (100, 255, 100)
SNAKE_HEAD = (50, 200, 50)
FOOD_COLOR = (255, 80, 80)
GRID_COLOR = (40, 40, 55)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (100, 200, 255)
SHADOW_COLOR = (0, 0, 0)

# Set display dimensions
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('🐍 Modern Snake Game')

# Set game clock
clock = pygame.time.Clock()

# Snake block size and speed
snake_block = 20
initial_speed = 10

# Font styles
title_font = pygame.font.SysFont("arial", 60, bold=True)
font_style = pygame.font.SysFont("arial", 25)
score_font = pygame.font.SysFont("arial", 30, bold=True)
small_font = pygame.font.SysFont("arial", 20)

# High score tracking
high_score = 0

def draw_grid():
    """Draw a subtle grid background"""
    for x in range(0, dis_width, snake_block):
        pygame.draw.line(dis, GRID_COLOR, (x, 0), (x, dis_height))
    for y in range(0, dis_height, snake_block):
        pygame.draw.line(dis, GRID_COLOR, (0, y), (dis_width, y))

def draw_text(text, font, color, x, y, center=False, shadow=False):
    """Helper function to draw text with optional shadow and centering"""
    if shadow:
        shadow_surf = font.render(text, True, SHADOW_COLOR)
        shadow_rect = shadow_surf.get_rect()
        if center:
            shadow_rect.center = (x + 2, y + 2)
        else:
            shadow_rect.topleft = (x + 2, y + 2)
        dis.blit(shadow_surf, shadow_rect)
    
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    dis.blit(text_surf, text_rect)

def display_score(score, high_score):
    """Display current score and high score with better styling"""
    # Current score
    score_text = f"Score: {score}"
    draw_text(score_text, score_font, TEXT_COLOR, 20, 20)
    
    # High score
    high_score_text = f"Best: {high_score}"
    draw_text(high_score_text, small_font, ACCENT_COLOR, 20, 60)

def draw_snake(snake_block, snake_list):
    """Draw snake with gradient effect and rounded head"""
    for i, segment in enumerate(snake_list):
        if i == len(snake_list) - 1:  # Head
            # Draw head with slight glow effect
            pygame.draw.circle(dis, SNAKE_HEAD, 
                             (int(segment[0] + snake_block/2), 
                              int(segment[1] + snake_block/2)), 
                             snake_block//2 + 2)
            # Eyes
            eye_size = 3
            pygame.draw.circle(dis, DARK_BG, 
                             (int(segment[0] + snake_block/2 - 5), 
                              int(segment[1] + snake_block/2 - 3)), eye_size)
            pygame.draw.circle(dis, DARK_BG, 
                             (int(segment[0] + snake_block/2 + 5), 
                              int(segment[1] + snake_block/2 - 3)), eye_size)
        else:  # Body
            # Gradient effect - segments get slightly darker toward tail
            color_factor = 0.7 + (i / len(snake_list)) * 0.3
            segment_color = (int(SNAKE_COLOR[0] * color_factor),
                           int(SNAKE_COLOR[1] * color_factor),
                           int(SNAKE_COLOR[2] * color_factor))
            pygame.draw.rect(dis, segment_color, 
                           [segment[0] + 1, segment[1] + 1, 
                            snake_block - 2, snake_block - 2], 
                           border_radius=5)

def draw_food(x, y, snake_block):
    """Draw food with pulsing animation"""
    pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
    size = snake_block // 2 + int(2 * pulse)
    
    # Outer glow
    pygame.draw.circle(dis, (255, 100, 100), 
                      (int(x + snake_block/2), int(y + snake_block/2)), 
                      size + 3)
    # Main food
    pygame.draw.circle(dis, FOOD_COLOR, 
                      (int(x + snake_block/2), int(y + snake_block/2)), 
                      size)

def game_intro():
    """Animated intro screen"""
    intro = True
    while intro:
        dis.fill(DARK_BG)
        draw_grid()
        
        # Title with shadow
        draw_text("SNAKE GAME", title_font, ACCENT_COLOR, 
                 dis_width/2, dis_height/3, center=True, shadow=True)
        
        # Instructions
        draw_text("Press SPACE to Start", font_style, TEXT_COLOR, 
                 dis_width/2, dis_height/2, center=True)
        draw_text("Press Q to Quit", font_style, TEXT_COLOR, 
                 dis_width/2, dis_height/2 + 40, center=True)
        
        # Controls
        draw_text("Use Arrow Keys to Move", small_font, (200, 200, 200), 
                 dis_width/2, dis_height - 100, center=True)
        
        # High score display
        if high_score > 0:
            draw_text(f"High Score: {high_score}", font_style, ACCENT_COLOR, 
                     dis_width/2, dis_height/2 + 100, center=True)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        clock.tick(15)

def game_over_screen(score, high_score):
    """Game over screen with better UI"""
    game_over = False
    while not game_over:
        dis.fill(DARK_BG)
        draw_grid()
        
        # Game Over title
        draw_text("GAME OVER", title_font, FOOD_COLOR, 
                 dis_width/2, dis_height/3 - 50, center=True, shadow=True)
        
        # Score display
        draw_text(f"Your Score: {score}", score_font, TEXT_COLOR, 
                 dis_width/2, dis_height/2, center=True)
        
        # New high score message
        if score == high_score and score > 0:
            draw_text("🏆 NEW HIGH SCORE! 🏆", font_style, ACCENT_COLOR, 
                     dis_width/2, dis_height/2 + 50, center=True)
        
        # Options
        draw_text("Press SPACE - Play Again", font_style, TEXT_COLOR, 
                 dis_width/2, dis_height - 120, center=True)
        draw_text("Press Q - Quit", font_style, TEXT_COLOR, 
                 dis_width/2, dis_height - 80, center=True)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    return True
        
        clock.tick(15)
    
    return False

def gameLoop():
    global high_score
    
    game_over = False
    game_close = False

    # Starting position - centered and aligned to grid
    x1 = dis_width // 2
    y1 = dis_height // 2
    x1 = round(x1 / snake_block) * snake_block
    y1 = round(y1 / snake_block) * snake_block

    # Change in position
    x1_change = 0
    y1_change = 0

    # Snake body
    snake_List = []
    Length_of_snake = 1

    # Food position - aligned to grid
    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    # Dynamic speed
    current_speed = initial_speed

    while not game_over:

        if game_close:
            if game_over_screen(Length_of_snake - 1, high_score):
                gameLoop()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Prevent 180-degree turns
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_ESCAPE:
                    game_close = True

        # Check if snake hits the boundary
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change
        
        # Draw background
        dis.fill(DARK_BG)
        draw_grid()

        # Draw food with animation
        draw_food(foodx, foody, snake_block)

        # Update snake
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        # Remove extra segments if snake hasn't eaten
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check if snake hits itself
        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        # Draw snake
        draw_snake(snake_block, snake_List)
        
        # Display score
        display_score(Length_of_snake - 1, high_score)

        pygame.display.update()

        # Check if snake eats food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            
            # Increase speed slightly as snake grows
            current_speed = min(initial_speed + Length_of_snake // 5, 25)
            
            # Update high score
            if Length_of_snake - 1 > high_score:
                high_score = Length_of_snake - 1

        clock.tick(current_speed)

    pygame.quit()
    quit()

# Start the game
game_intro()
gameLoop()