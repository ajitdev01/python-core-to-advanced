import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 900
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Colors - Modern Dark Theme
BG_COLOR = (28, 28, 40)
LINE_COLOR = (50, 50, 70)
CIRCLE_COLOR = (100, 200, 255)
CROSS_COLOR = (255, 100, 100)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (60, 60, 80)
BUTTON_HOVER = (80, 80, 100)
ACCENT_COLOR = (100, 200, 255)
WIN_LINE_COLOR = (255, 215, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('🎮 Tic-Tac-Toe Ultimate')

# Fonts
title_font = pygame.font.SysFont('arial', 60, bold=True)
font = pygame.font.SysFont('arial', 40)
small_font = pygame.font.SysFont('arial', 30)
tiny_font = pygame.font.SysFont('arial', 20)

# Game variables
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
game_mode = None  # 'PVP' or 'PVC'
current_player = 1  # 1 for X, 2 for O
game_over = False
winner = None
winning_line = None
scores = {'X': 0, 'O': 0, 'Draws': 0}

# Board offset for centering
BOARD_OFFSET_X = (WIDTH - BOARD_COLS * SQUARE_SIZE) // 2
BOARD_OFFSET_Y = 150

class Button:
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
    
    def draw(self, screen):
        color = BUTTON_HOVER if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, ACCENT_COLOR, self.rect, 3, border_radius=10)
        
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def is_hovered(self, pos):
        self.hover = self.rect.collidepoint(pos)
        return self.hover
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_text(text, font, color, x, y, center=True):
    text_surf = font.render(text, True, color)
    if center:
        text_rect = text_surf.get_rect(center=(x, y))
    else:
        text_rect = text_surf.get_rect(topleft=(x, y))
    screen.blit(text_surf, text_rect)

def draw_lines():
    # Horizontal lines
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(
            screen, 
            LINE_COLOR, 
            (BOARD_OFFSET_X, BOARD_OFFSET_Y + row * SQUARE_SIZE), 
            (BOARD_OFFSET_X + WIDTH - 2 * BOARD_OFFSET_X, BOARD_OFFSET_Y + row * SQUARE_SIZE), 
            LINE_WIDTH
        )
    
    # Vertical lines
    for col in range(1, BOARD_COLS):
        pygame.draw.line(
            screen, 
            LINE_COLOR, 
            (BOARD_OFFSET_X + col * SQUARE_SIZE, BOARD_OFFSET_Y), 
            (BOARD_OFFSET_X + col * SQUARE_SIZE, BOARD_OFFSET_Y + HEIGHT - BOARD_OFFSET_Y - 250), 
            LINE_WIDTH
        )

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # X
                # Draw X
                start_desc = (
                    BOARD_OFFSET_X + col * SQUARE_SIZE + SPACE,
                    BOARD_OFFSET_Y + row * SQUARE_SIZE + SPACE
                )
                end_desc = (
                    BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                    BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE - SPACE
                )
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                
                start_asc = (
                    BOARD_OFFSET_X + col * SQUARE_SIZE + SPACE,
                    BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE - SPACE
                )
                end_asc = (
                    BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                    BOARD_OFFSET_Y + row * SQUARE_SIZE + SPACE
                )
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
                
            elif board[row][col] == 2:  # O
                center = (
                    BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2,
                    BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                )
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_win(player):
    # Check rows
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True, ('row', row)
    
    # Check columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True, ('col', col)
    
    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return True, ('diag', 'main')
    
    if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True, ('diag', 'anti')
    
    return False, None

def draw_winning_line(line_type, index):
    if line_type == 'row':
        start_pos = (BOARD_OFFSET_X + 20, BOARD_OFFSET_Y + index * SQUARE_SIZE + SQUARE_SIZE // 2)
        end_pos = (BOARD_OFFSET_X + WIDTH - 2 * BOARD_OFFSET_X - 20, BOARD_OFFSET_Y + index * SQUARE_SIZE + SQUARE_SIZE // 2)
    elif line_type == 'col':
        start_pos = (BOARD_OFFSET_X + index * SQUARE_SIZE + SQUARE_SIZE // 2, BOARD_OFFSET_Y + 20)
        end_pos = (BOARD_OFFSET_X + index * SQUARE_SIZE + SQUARE_SIZE // 2, BOARD_OFFSET_Y + 3 * SQUARE_SIZE - 20)
    elif line_type == 'diag' and index == 'main':
        start_pos = (BOARD_OFFSET_X + 20, BOARD_OFFSET_Y + 20)
        end_pos = (BOARD_OFFSET_X + 3 * SQUARE_SIZE - 20, BOARD_OFFSET_Y + 3 * SQUARE_SIZE - 20)
    else:  # anti-diagonal
        start_pos = (BOARD_OFFSET_X + 3 * SQUARE_SIZE - 20, BOARD_OFFSET_Y + 20)
        end_pos = (BOARD_OFFSET_X + 20, BOARD_OFFSET_Y + 3 * SQUARE_SIZE - 20)
    
    pygame.draw.line(screen, WIN_LINE_COLOR, start_pos, end_pos, 15)

def restart_game():
    global board, current_player, game_over, winner, winning_line
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    current_player = 1
    game_over = False
    winner = None
    winning_line = None

def minimax(board_state, depth, is_maximizing, alpha, beta):
    """AI algorithm with alpha-beta pruning"""
    # Check terminal states
    win, _ = check_win(2)  # AI is player 2 (O)
    if win:
        return 10 - depth
    
    win, _ = check_win(1)  # Human is player 1 (X)
    if win:
        return depth - 10
    
    if is_board_full():
        return 0
    
    if is_maximizing:
        max_eval = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board_state[row][col] is None:
                    board_state[row][col] = 2
                    eval = minimax(board_state, depth + 1, False, alpha, beta)
                    board_state[row][col] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board_state[row][col] is None:
                    board_state[row][col] = 1
                    eval = minimax(board_state, depth + 1, True, alpha, beta)
                    board_state[row][col] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move():
    """Find the best move for AI"""
    best_score = -math.inf
    move = None
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 2
                score = minimax(board, 0, False, -math.inf, math.inf)
                board[row][col] = None
                
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    return move

def draw_scoreboard():
    """Draw the scoreboard at the bottom"""
    y_pos = HEIGHT - 120
    
    # Background panel
    panel_rect = pygame.Rect(50, y_pos - 20, WIDTH - 100, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, panel_rect, border_radius=15)
    pygame.draw.rect(screen, ACCENT_COLOR, panel_rect, 3, border_radius=15)
    
    # Scores
    x_offset = WIDTH // 4
    draw_text(f"X Wins: {scores['X']}", small_font, CROSS_COLOR, x_offset, y_pos + 20)
    draw_text(f"Draws: {scores['Draws']}", small_font, TEXT_COLOR, WIDTH // 2, y_pos + 20)
    draw_text(f"O Wins: {scores['O']}", small_font, CIRCLE_COLOR, WIDTH - x_offset, y_pos + 20)

def mode_selection_screen():
    """Screen to select game mode"""
    pvp_button = Button(WIDTH // 2 - 200, 300, 400, 80, "Player vs Player")
    pvc_button = Button(WIDTH // 2 - 200, 420, 400, 80, "Player vs Computer")
    
    selecting = True
    while selecting:
        screen.fill(BG_COLOR)
        
        # Title
        draw_text("TIC-TAC-TOE", title_font, ACCENT_COLOR, WIDTH // 2, 120)
        draw_text("Choose Game Mode", font, TEXT_COLOR, WIDTH // 2, 200)
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        pvp_button.is_hovered(mouse_pos)
        pvc_button.is_hovered(mouse_pos)
        
        # Draw buttons
        pvp_button.draw(screen)
        pvc_button.draw(screen)
        
        # Instructions
        draw_text("Player 1: X (Red) | Player 2: O (Blue)", tiny_font, (150, 150, 150), WIDTH // 2, 550)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_button.is_clicked(mouse_pos):
                    return 'PVP'
                if pvc_button.is_clicked(mouse_pos):
                    return 'PVC'
        
        pygame.display.update()

def main():
    global current_player, game_over, winner, winning_line, game_mode, scores
    
    clock = pygame.time.Clock()
    
    # Mode selection
    game_mode = mode_selection_screen()
    
    restart_button = Button(WIDTH // 2 - 100, HEIGHT - 200, 200, 60, "Restart")
    menu_button = Button(50, 50, 150, 50, "Menu")
    
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        restart_button.is_hovered(mouse_pos)
        menu_button.is_hovered(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                # Menu button
                if menu_button.is_clicked(mouse_pos):
                    game_mode = mode_selection_screen()
                    restart_game()
                    scores = {'X': 0, 'O': 0, 'Draws': 0}
                    continue
                
                # Only allow human input on their turn
                if game_mode == 'PVC' and current_player == 2:
                    continue
                
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                
                clicked_row = (mouseY - BOARD_OFFSET_Y) // SQUARE_SIZE
                clicked_col = (mouseX - BOARD_OFFSET_X) // SQUARE_SIZE
                
                if 0 <= clicked_row < BOARD_ROWS and 0 <= clicked_col < BOARD_COLS:
                    if available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, current_player)
                        
                        # Check for win
                        win, line = check_win(current_player)
                        if win:
                            game_over = True
                            winner = current_player
                            winning_line = line
                            if current_player == 1:
                                scores['X'] += 1
                            else:
                                scores['O'] += 1
                        elif is_board_full():
                            game_over = True
                            scores['Draws'] += 1
                        
                        # Switch player
                        current_player = 2 if current_player == 1 else 1
            
            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if restart_button.is_clicked(mouse_pos):
                    restart_game()
        
        # AI move
        if game_mode == 'PVC' and current_player == 2 and not game_over:
            pygame.time.delay(500)  # Add slight delay for better UX
            move = best_move()
            if move:
                mark_square(move[0], move[1], 2)
                
                # Check for win
                win, line = check_win(2)
                if win:
                    game_over = True
                    winner = 2
                    winning_line = line
                    scores['O'] += 1
                elif is_board_full():
                    game_over = True
                    scores['Draws'] += 1
                
                current_player = 1
        
        # Drawing
        screen.fill(BG_COLOR)
        
        # Header
        mode_text = "Player vs Player" if game_mode == 'PVP' else "Player vs Computer"
        draw_text(mode_text, small_font, ACCENT_COLOR, WIDTH // 2, 70)
        
        # Current player or winner
        if not game_over:
            player_text = "X's Turn" if current_player == 1 else "O's Turn"
            player_color = CROSS_COLOR if current_player == 1 else CIRCLE_COLOR
            draw_text(player_text, font, player_color, WIDTH // 2, 110)
        else:
            if winner:
                winner_text = f"{'X' if winner == 1 else 'O'} Wins!"
                winner_color = CROSS_COLOR if winner == 1 else CIRCLE_COLOR
                draw_text(winner_text, font, winner_color, WIDTH // 2, 110)
            else:
                draw_text("It's a Draw!", font, TEXT_COLOR, WIDTH // 2, 110)
        
        # Draw game elements
        draw_lines()
        draw_figures()
        
        # Draw winning line
        if game_over and winner and winning_line:
            draw_winning_line(winning_line[0], winning_line[1])
        
        # Draw buttons
        menu_button.draw(screen)
        if game_over:
            restart_button.draw(screen)
        
        # Draw scoreboard
        draw_scoreboard()
        
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()