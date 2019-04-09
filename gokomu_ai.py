import random
import pygame
import os
#os.environ['SDL_VIDEODRIVER']='dummy'

# initialize pygame


# initialize mixer （since we would use music）
#pygame.mixer.init()

# initialize screen size and titile



pygame.init()
pygame.mixer.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
font_name = pygame. font.get_default_font()

WIDTH = 720
GRID_WIDTH = WIDTH // 16
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GOKOMU")
# set a clock to save CPU resource
FPS = 15
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

# load background image
background_img = pygame.image.load('images/back.png')
movements =[]
running = True



def num_2_gridpos(num):
    return (1 + (num % 15), (num // 15) + 1)

def gridpos_2_num(grid):
    return (grid[1] - 1) * 15 + grid[0] - 1


def around_grid(curr_move_pos, step=2):
    left = curr_move_pos[0] - step if (curr_move_pos[0] - step) > 0 else 1
    right = curr_move_pos[0] + step if (curr_move_pos[0] + step) < 16 else 15
    top = curr_move_pos[1] - step if (curr_move_pos[1] - step) > 0 else 1
    bottom = curr_move_pos[1] + step if (curr_move_pos[1] + step) < 16 else 15
    
    return (left, right, top, bottom)

def add_stone(screen, color,pos,ident):
    num_pos = gridpos_2_num(pos)
    remain.remove(num_pos)
    movements.append(((pos[0] * GRID_WIDTH, pos[1] * GRID_WIDTH), color))
    if num_pos in player_optimal_set:
        player_optimal_set.remove(num_pos)

    player_score_matrix[pos[0]][pos[1]] = -1 - ident
    ai_score_matrix[pos[0]][pos[1]] = -1 - ident
    color_matrix[pos[0]][pos[1]] = color
    pygame.draw.circle(screen, color,(pos[0] * GRID_WIDTH, pos[1] * GRID_WIDTH), 15)
    around = around_grid(pos, 4)
    # print(around)
    #print(ai_score_matrix)
    for rx in range(around[0], around[1] + 1):
        for ry in range(around[2], around[3] + 1):
            num_pos = gridpos_2_num((rx, ry))
            if num_pos in remain:
                update_score((rx, ry), color, ident)
                if color == BLACK:
                    tpcolor = WHITE
                else:
                    tpcolor = BLACK
                update_score((rx, ry), tpcolor, 1 - ident)


#print('\n')
        





def draw_movements(surf):
    for m in movements:
        # m[0] stores position，m[1] stores color
        pygame.draw.circle(surf, m[1], m[0], 15)

def draw_background(surf):
    #background figure
    # draw player and computer
    Background=background_img.convert_alpha()
    s_font = pygame.font.SysFont("comicsansms", 35)
    text1 = s_font.render("You", 1, BLACK)
    text2 = s_font.render("AI", 1, BLACK)
    surf.blit(Background, (0, 0))
    surf.blit(text1, (WIDTH//2+90, WIDTH))
    surf.blit(text2, (200, WIDTH))
    pygame.draw.circle(surf,BLACK, (WIDTH//2+50,WIDTH+5),20)
    pygame.draw.circle(surf,WHITE, (150,WIDTH+5),20)
    # draw grid line 15x15
    # 1. draw border，GRID_WIDTH = WIDTH // 16
   
    rect_lines = [
        ((GRID_WIDTH, GRID_WIDTH), (GRID_WIDTH, WIDTH - GRID_WIDTH)),
        ((GRID_WIDTH, GRID_WIDTH), (WIDTH - GRID_WIDTH, GRID_WIDTH)),
        ((GRID_WIDTH, WIDTH - GRID_WIDTH),
            (WIDTH - GRID_WIDTH, WIDTH - GRID_WIDTH)),
        ((WIDTH - GRID_WIDTH, GRID_WIDTH),
            (WIDTH - GRID_WIDTH, WIDTH - GRID_WIDTH)),
    ]
    for line in rect_lines:
        pygame.draw.line(surf, BLACK, line[0], line[1], 2)

    # draw inner grid lines
    for i in range(13):
        pygame.draw.line(surf, BLACK,
                         (GRID_WIDTH * (2 + i), GRID_WIDTH),
                         (GRID_WIDTH * (2 + i), WIDTH - GRID_WIDTH))
        pygame.draw.line(surf, BLACK,
                         (GRID_WIDTH, GRID_WIDTH * (2 + i)),
                         (WIDTH - GRID_WIDTH, GRID_WIDTH * (2 + i)))

    # draw 5 points on the board
    circle_center = [
        (GRID_WIDTH * 4, GRID_WIDTH * 4),
        (WIDTH - GRID_WIDTH * 4, GRID_WIDTH * 4),
        (WIDTH - GRID_WIDTH * 4, WIDTH - GRID_WIDTH * 4),
        (GRID_WIDTH * 4, WIDTH - GRID_WIDTH * 4),
        (GRID_WIDTH * 8, GRID_WIDTH * 8)
    ]
    for cc in circle_center:
        pygame.draw.circle(surf, BLACK, cc, 5)

def game_is_over(pos, color): #Judge whether the game ends
    hori = 1
    verti = 1
    slash = 1
    backslash = 1
    left = pos[0] - 1
    while left > 0 and color_matrix[left][pos[1]] == color:
        left -= 1
        hori += 1
    
    right = pos[0] + 1
    while right < 16 and color_matrix[right][pos[1]] == color:
        right += 1
        hori += 1
    
    up = pos[1] - 1
    while up > 0 and color_matrix[pos[0]][up] == color:
        up -= 1
        verti += 1
    
    down = pos[1] + 1
    while down < 16 and color_matrix[pos[0]][down] == color:
        down += 1
        verti += 1
    
    left = pos[0] - 1
    up = pos[1] - 1
    while left > 0 and up > 0 and color_matrix[left][up] == color:
        left -= 1
        up -= 1
        backslash += 1
    
    right = pos[0] + 1
    down = pos[1] + 1
    while right < 16 and down < 16 and color_matrix[right][down] == color:
        right += 1
        down += 1
        backslash += 1
    
    right = pos[0] + 1
    up = pos[1] - 1
    while right < 16 and up > 0 and color_matrix[right][up] == color:
        right += 1
        up -= 1
        slash += 1
    
    left = pos[0] - 1
    down = pos[1] + 1
    while left > 0 and down < 16 and color_matrix[left][down] == color:
        left -= 1
        down += 1
        slash += 1

    if max([hori, verti, backslash, slash]) >= 5:
        return True

def update_score(pos, color, ident): #update the score after each move
    hori = 1
    verti = 1
    slash = 1
    backslash = 1
    left = pos[0] - 1
    
    while left > 0 and color_matrix[left][pos[1]] == color:
        left -= 1
        if hori == 4:
            hori += 1
            break
        if left > 0 and\
            (color_matrix[left][pos[1]] == color or
             color_matrix[left][pos[1]] is None):
            hori += 1

    right = pos[0] + 1
    while right < 16 and color_matrix[right][pos[1]] == color:
        right += 1
        if hori == 4:
            hori += 1
            break
        if right < 16 and\
            (color_matrix[right][pos[1]] == color or
                color_matrix[right][pos[1]] is None):
            hori += 1

    hori = score_level[hori]

    up = pos[1] - 1
    while up > 0 and color_matrix[pos[0]][up] == color:
        up -= 1
        if verti == 4:
            verti += 1
            break
        if up > 0 and\
            (color_matrix[pos[0]][up] == color or
                color_matrix[pos[0]][up] is None):
            verti += 1

    down = pos[1] + 1
    while down < 16 and color_matrix[pos[0]][down] == color:
        down += 1
        if verti == 4:
            verti += 1
            break
        if down < 16 and\
            (color_matrix[pos[0]][down] == color or
             color_matrix[pos[0]][down] is None):
            verti += 1

    verti = score_level[verti]

    left = pos[0] - 1
    up = pos[1] - 1
    while left > 0 and up > 0 and color_matrix[left][up] == color:
        left -= 1
        up -= 1
        if backslash == 4:
            backslash += 1
            break
        if left > 0 and up > 0 and\
            (color_matrix[left][up] == color or
                color_matrix[left][up] is None):
            backslash += 1

    right = pos[0] + 1
    down = pos[1] + 1
    while right < 16 and down < 16 and color_matrix[right][down] == color:
        right += 1
        down += 1
        if backslash == 4:
            backslash += 1
            break
        if right < 16 and down < 16 and\
            (color_matrix[right][down] == color or
                color_matrix[right][down] is None):
            backslash += 1
    backslash = score_level[backslash]

    right = pos[0] + 1
    up = pos[1] - 1
    while right < 16 and up > 0 and color_matrix[right][up] == color:
        right += 1
        up -= 1
        if slash == 4:
            slash += 1
            break
        if right < 16 and up > 0 and (color_matrix[right][up] == color or
                                      color_matrix[right][up] is None):
            slash += 1

    left = pos[0] - 1
    down = pos[1] + 1
    while left > 0 and down < 16 and color_matrix[left][down] == color:
        left -= 1
        down += 1
        if slash == 4:
            slash += 1
            break
        if left > 0 and down < 16 and (color_matrix[left][down] == color or
                                   color_matrix[left][down] is None):
            slash += 1

    slash = score_level[slash]
# print(pos, color, ident, (hori, verti, slash, backslash))

    if ident == USER:
        player_score_matrix[pos[0]][pos[1]] =\
            int((hori + verti + slash + backslash) * 0.9)
    else:
        ai_score_matrix[pos[0]][pos[1]] = hori + verti + slash + backslash


def move(surf,pos): # Move stone
   
    grid = (int(round(pos[0] / (GRID_WIDTH + .0))),
            int(round(pos[1] / (GRID_WIDTH + .0))))
        
    if grid[0] <= 0 or grid[0] > 15:
        return
    if grid[1] <= 0 or grid[1] > 15:
        return
            
    pos = (grid[0] * GRID_WIDTH, grid[1] * GRID_WIDTH)

# num_pos = gridpos_2_num(grid)
# if num_pos not in remain:
#     return None
    if color_matrix[grid[0]][grid[1]] is not None:
        return None
    
    curr_move = (pos, BLACK)
    add_stone(surf, BLACK, grid, USER)
    for rx in range(16):
        print(ai_score_matrix[rx])
    if game_is_over(grid, BLACK):
        return (False, USER)
    
    return respond(surf, movements, curr_move)



def mcts(surf, movements, think_time):
    Node = []
    record = []
    current_root = movements
    record.append(current_root)
    board = surf #make a copy of the game board
    
    return 0

def get_next_move(movements, curr_move):
    around = around_grid((curr_move[0][0] // GRID_WIDTH,
                          curr_move[0][1] // GRID_WIDTH))
        
    for rx in range(around[0], around[1] + 1):
        for ry in range(around[2], around[3] + 1):
            num_pos = gridpos_2_num((rx, ry))
            if num_pos in remain:
                player_optimal_set.add(gridpos_2_num((rx, ry)))

    max_score = -1000000
    next_move = 0
    for i in player_optimal_set:
        grid = num_2_gridpos(i)
        if ai_score_matrix[grid[0]][grid[1]] >= score_level[5]:
            next_move = i
            break
        if player_score_matrix[grid[0]][grid[1]] >= score_level[4]:
            next_move = i
            break
        score = ai_score_matrix[grid[0]][grid[1]] +\
            player_score_matrix[grid[0]][grid[1]]
        
        if max_score < score:
            max_score = score
            next_move = i
        elif max_score == score:
            if (random.randint(0, 100) % 2) == 0:
                next_move = i

    around = around_grid(num_2_gridpos(next_move))

    for rx in range(around[0], around[1] + 1):
        for ry in range(around[2], around[1] + 1):
            num_pos = gridpos_2_num((rx, ry))
            if num_pos in remain:
                player_optimal_set.add(gridpos_2_num((rx, ry)))
    return next_move

def respond(surf,movements,curr_move):
    #grid_pos = mcts(surf, movements, 90)
    grid_pos = num_2_gridpos(get_next_move(movements, curr_move))
    #grid_pos = (random.randint(1, 15), random.randint(1, 15))
    # print(grid_pos)
    add_stone(surf, WHITE, grid_pos,AI)
    
    if game_is_over(grid_pos, WHITE):
        return (False, AI)
    
    return None


def draw_notification(surf, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont("comicsansms", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def over_screen(surf, winner):
    note_height = 8
    if winner is not None:
        draw_notification(surf, 'You {0} '.format('win' if winner == USER else 'lose!'),
                  64, WIDTH // 2, note_height, RED)
    else:
        screen.blit(background, back_rect)
    
    
    draw_notification(surf, 'Click anywhere to re-start', 50, WIDTH // 2, note_height + WIDTH // 2,
              GREEN)
    pygame.display.flip()
    waiting = True
    
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:#press any key to restart
                waiting = False


USER, AI = 1, 0
winner = None
#Store score for both player and AI
player_score_matrix = [[0] * 16 for i in range(16)]
ai_score_matrix = [[0] * 16 for i in range(16)]
score_level = [0, 1, 10, 100, 1000, 10000, 100000, 1000000, 1000000]
player_optimal_set = set()
# We need a matrix to record the color of each position
color_matrix = [[None] * 16 for i in range(16)]
game_over = False
running = True
remain = set(range(1, 15**2 + 1))
while running:
    
    # Set update frequency
    clock.tick(FPS)
    
    
    # deal with different events
    for event in pygame.event.get():
        
    # check whether the windwo is closed
        if event.type == pygame.QUIT:
            running = False
        #when clicking mouse, put a stone
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            response = move(screen,event.pos)
            if response is not None and response[0] is False:
                game_over = True
                winner = response[1]
                continue
    if game_over == True:
        over_screen(screen, winner)
        game_over = False
        movements = []
        remain = set(range(1, 15**2 + 1))
        
        #Reset the game
        player_score_matrix = [[0] * 16 for i in range(16)]
        ai_score_matrix = [[0] * 16 for i in range(16)]#reset score matrix
        color_matrix = [[None] * 16 for i in range(16)]
        
        ai_possible_list = []
        ai_optimal_list = []
        ai_tabu_list = []
        player_optimal_set = set()
        player_tabu_list = []

    # draw board
    #all_sprites.update()
    #all_sprites.draw(screen)
    draw_background(screen)
    draw_movements(screen)

    # update screen
    # After drawing everything, flip the display
    pygame.display.flip()


