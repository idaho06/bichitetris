import random
import sys
import pygame as pg

""" 
  ______                _   _                 
 |  ____|              | | (_)                
 | |__ _   _ _ __   ___| |_ _  ___  _ __  ___ 
 |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
 | |  | |_| | | | | (__| |_| | (_) | | | \__ \ 
 |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
                                              
                                               """


def blit_board():
    global screen
    global board_posx
    global board_posy
    global board
    global block_colors
    i = 0
    for row in board:
        j = 0
        for block_index in row:
            block = block_colors[block_index]
            block_rect = block.get_rect()
            block_rect.x = board_posx + (16*j)
            block_rect.y = board_posy + (16*i)
            screen.blit(block, block_rect)
            j += 1
        i += 1


def blit_piece(piece, color, row, column):
    global screen
    global board_posx
    global board_posy
    global block_colors
    block = block_colors[color]
    block_rect = block.get_rect()
    for pos in piece:
        x, y = pos
        block_rect.x = board_posx + (16*(column+x))
        block_rect.y = board_posy + (16*(row+y))
        screen.blit(block, block_rect)


def blit_next_piece(piece, color):
    global screen
    global block_colors
    global next_piece_posx
    global next_piece_posy
    block = block_colors[color]
    block_rect = block.get_rect()
    for pos in piece:
        x, y = pos
        block_rect.x = next_piece_posx + (16*x)
        block_rect.y = next_piece_posy + (16*y)
        screen.blit(block, block_rect)


def move_piece_left(piece):
    global piece_pos_row
    global piece_pos_col
    if not is_piece_occupied(piece, piece_pos_row, (piece_pos_col - 1)):
        piece_pos_col -= 1


def move_piece_right(piece):
    global piece_pos_row
    global piece_pos_col
    if not is_piece_occupied(piece, piece_pos_row, (piece_pos_col + 1)):
        piece_pos_col += 1


def move_piece_down(piece):
    global piece_pos_row
    global piece_pos_col
    if not is_piece_occupied(piece, (piece_pos_row + 1), piece_pos_col):
        piece_pos_row += 1
    else:
        pg.event.post(pg.event.Event(PIECE_HIT, {}))


def move_piece_rotate_cw(pieces):
    global piece_rotation
    global piece_pos_row
    global piece_pos_col
    rotations = len(pieces)
    next_rotation = piece_rotation
    if (next_rotation + 1) < rotations:
        next_rotation += 1
    else:
        next_rotation = 0
    if not is_piece_occupied(pieces[next_rotation], piece_pos_row, piece_pos_col):
        piece_rotation = next_rotation


def is_piece_occupied(piece, row, column):
    global board
    global columns
    global rows
    collision = False
    for pos in piece:
        x, y = pos
        x = column + x
        y = row + y
        if x < 0 or x > (columns - 1):
            return True
        if y > (rows - 1):
            return True
        content = board[y][x]
        if content != 0:
            collision = True
    return collision


def copy_piece_to_board(piece, color, row, column):
    global board
    for pos in piece:
        x, y = pos
        x = column + x
        y = row + y
        board[y][x] = color


def random_piece():
    global pieces
    return random.choice(pieces)


def get_next_piece():
    global next_piece
    global next_piece_color
    global current_piece
    global current_piece_color
    current_piece = next_piece
    current_piece_color = next_piece_color
    any_piece = random_piece()
    next_piece = any_piece["piece"]
    next_piece_color = any_piece["color"]


def detect_full_rows():
    global board
    full_rows = []
    for row in board:
        if 0 not in row:
            full_rows.insert(0, board.index(row))
    return full_rows


def delete_full_rows():
    global board
    global lines
    full_rows = detect_full_rows()
    num_rows = len(full_rows)
    if num_rows == 0:
        play_sound_hit()
        return
    for full_row_index in full_rows:
        del board[full_row_index]
    for j in range(num_rows):
        new_row = [0 for i in range(columns)]
        board.insert(0, new_row)
    lines += num_rows
    update_lines_text()
    play_sound_lines(num_rows)


def update_lines_text():
    global lines
    global text_number_white
    global text_number_white_rect
    #global jamma_font_tall
    #del text_number_white_rect
    #del text_number_white
    #text_number_white = jamma_font_tall.render(
    #    str(lines).zfill(4), False, white).convert_alpha()
    text_number_white = surface_text_shadow(str(lines).zfill(4), white, tall=True)
    text_number_white_rect = text_number_white.get_rect()
    text_number_white_rect.x = lines_piece_posx - 16
    text_number_white_rect.y = lines_piece_posy


def set_level():
    global speed
    global lines
    global background
    global background_rect
    if lines > 7 and speed > 900:
        speed = 900
        pg.mixer.music.load(filename="snd/level2.ogg")
        pg.mixer.music.play(loops=-1)
        change_background(2)
    if lines > 15 and speed > 800:
        speed = 800
        pg.mixer.music.load(filename="snd/level3.ogg")
        pg.mixer.music.play(loops=-1)
        change_background(3)
    if lines > 23 and speed > 700:
        speed = 700
        pg.mixer.music.load(filename="snd/level4.ogg")
        pg.mixer.music.play(loops=-1)
        change_background(4)
    if lines > 31 and speed > 600:
        speed = 600
        pg.mixer.music.load(filename="snd/level5.ogg")
        pg.mixer.music.play(loops=-1)
        change_background(5)
    if lines > 39 and speed > 500:
        speed = 500
        pg.mixer.music.load(filename="snd/level6.ogg")
        pg.mixer.music.play(loops=-1)
        change_background(6)
    if lines > 47 and speed > 350:
        speed = 350
        pg.mixer.music.load(filename="snd/level7.ogg")
        pg.mixer.music.play(loops=-1)
        change_background(7)
    if lines > 55 and speed > 200:
        speed = 200
        pg.mixer.music.load(filename="snd/level8.ogg")
        pg.mixer.music.play(loops=-1)
        change_background(8)
    if lines > 63 and speed > 100:
        speed = 100


def play_sound_lines(num_rows):
    global sound_line1
    global sound_line2
    global sound_line3
    global sound_line4
    if num_rows <= 0:
        return
    if num_rows == 1:
        sound_line1.play()
    if num_rows == 2:
        sound_line2.play()
    if num_rows == 3:
        sound_line3.play()
    if num_rows >= 4:
        sound_line4.play()


def play_sound_hit():
    global sound_hit
    sound_hit.play()


def blit_text_next():
    global text_next_white
    global text_next_white_rect
    screen.blit(text_next_white, text_next_white_rect)


def blit_text_lines():
    global text_lines_white
    global text_lines_white_rect
    screen.blit(text_lines_white, text_lines_white_rect)


def reset_game():
    global background
    global background_rect
    global lines
    global speed
    global start_speed
    global board
    pg.time.set_timer(PIECE_FALL, speed)
    pg.mixer.music.load(filename="snd/level1.ogg")
    pg.mixer.music.play(loops=-1)
    background = pg.image.load("img/background01.png").convert()
    background_rect = background.get_rect()
    lines = 0
    update_lines_text()
    speed = start_speed
    for row in board:
        j = 0
        for block_index in row:
            row[j] = 0
            j += 1


def change_background(num: int):
    global background
    global background_rect
    if num <= 1:
        background = pg.image.load("img/background01.png").convert()
        background_rect = background.get_rect()
    if num == 2:
        background = pg.image.load("img/background02.png").convert()
        background_rect = background.get_rect()
    if num == 3:
        background = pg.image.load("img/background03.png").convert()
        background_rect = background.get_rect()
    if num == 4:
        background = pg.image.load("img/background04.png").convert()
        background_rect = background.get_rect()
    if num == 5:
        background = pg.image.load("img/background05.png").convert()
        background_rect = background.get_rect()
    if num == 6:
        background = pg.image.load("img/background06.png").convert()
        background_rect = background.get_rect()
    if num == 7:
        background = pg.image.load("img/background07.png").convert()
        background_rect = background.get_rect()
    if num >= 8:
        background = pg.image.load("img/background08.png").convert()
        background_rect = background.get_rect()


def surface_text_shadow(text, color, tall = False):
    global jamma_font_short
    global jamma_font_tall
    global font_size
    shadow_color = 0,0,0
    if tall:
        font = jamma_font_tall
        displacement = font_size
    else:
        font = jamma_font_short
        displacement = font_size
    shadow_surface = font.render(text, False, shadow_color)
    shadow_surface.set_alpha(128)
    shadow_surface_rect = shadow_surface.get_rect()
    shadow_surface_rect.x = displacement
    shadow_surface_rect.y = displacement
    text_surface = font.render(text, False, color)
    result_width = text_surface.get_width()+displacement
    result_height = text_surface.get_height()+displacement
    result_surface = pg.Surface((result_width, result_height), pg.SRCALPHA)
    result_surface.blit(shadow_surface,shadow_surface_rect)
    result_surface.blit(text_surface,text_surface.get_rect())
    return result_surface.convert_alpha()

def surface_text_box(text_array):
    global jamma_font_short
    global jamma_font_tall
    global font_size
    shadow_color = 0,0,0
    pad = font_size*8
    text_surfaces = []
    for line in text_array:
        text_surfaces.append(surface_text_shadow(line[0], line[1], line[2]))
    # get width
    result_width = 0
    for surface in text_surfaces:
        if result_width < surface.get_width():
            result_width = surface.get_width()
    result_width += pad*2
    # get height
    result_height = pad*2
    for surface in text_surfaces:
        result_height += surface.get_height()
    result_surface = pg.Surface((result_width, result_height), pg.SRCALPHA)
    # paint it black and set alpha to 128
    result_surface.fill((0,0,0,128))
    # blit texts inside
    y = pad
    for surface in text_surfaces:
        surface_rect = surface.get_rect()
        surface_rect.x = pad
        surface_rect.y = y
        result_surface.blit(surface, surface_rect)
        y += surface_rect.h
    return result_surface.convert_alpha()
    


""" 
 __      __        _       _     _           
 \ \    / /       (_)     | |   | |          
  \ \  / /_ _ _ __ _  __ _| |__ | | ___  ___ 
   \ \/ / _` | '__| |/ _` | '_ \| |/ _ \/ __|
    \  / (_| | |  | | (_| | |_) | |  __/\__ \ 
     \/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/
                                             
                                              """

pg.init()

done = False

game_status = "ATRACT"  # ATRACT, GAME, GAME_OVER

size = width, height = 640, 480
black = 0, 0, 0
white = 255, 255, 255


screen = pg.display.set_mode(vsync=1, size=size, flags=pg.SCALED)
pg.display.toggle_fullscreen()
pg.display.set_caption("BichiTetris")
pg.display.set_icon(pg.image.load("img/icon.png"))

columns = 10
rows = 20
board = [[0 for i in range(columns)] for j in range(rows)]
board_posx = 240
board_posy = 80
#board[0][0] = 1
#board[19][0] = 1
#board[19][9] = 1
#board[0][9] = 1

next_piece_posx = 128
next_piece_posy = 150

lines_piece_posx = 128
lines_piece_posy = 300

piece_pos_col_start = 5
piece_pos_row_start = 1

piece_pos_col = piece_pos_col_start
piece_pos_row = piece_pos_row_start
piece_rotation = 0


block_colors = [
    pg.image.load("img/black.png").convert_alpha(),
    pg.image.load("img/block_blue.png").convert_alpha(),
    pg.image.load("img/block_green.png").convert_alpha(),
    pg.image.load("img/block_orange.png").convert_alpha(),
    pg.image.load("img/block_pink.png").convert_alpha(),
    pg.image.load("img/block_purple.png").convert_alpha(),
    pg.image.load("img/block_red.png").convert_alpha(),
    pg.image.load("img/block_yellow.png").convert_alpha(),
]

box01 = [(0, 0), (1, 0), (0, 1), (1, 1)]

el01 = [(0, -1), (0, 0), (0, 1), (1, 1)]
el02 = [(-1, 0), (0, 0), (1, 0), (-1, 1)]
el03 = [(0, -1), (1, -1), (1, 0), (1, 1)]
el04 = [(-1, 1), (0, 1), (1, 1), (1, 0)]

jay01 = [(1, -1), (1, 0), (1, 1), (0, 1)]
jay02 = [(-1, 0), (-1, 1), (0, 1), (1, 1)]
jay03 = [(0, -1), (0, 0), (0, 1), (1, -1)]
jay04 = [(-1, 0), (0, 0), (1, 0), (1, 1)]

zee01 = [(-1, 0), (0, 0), (0, 1), (1, 1)]
zee02 = [(1, -1), (0, 0), (1, 0), (0, 1)]

ess01 = [(-1, 1), (0, 0), (0, 1), (1, 0)]
ess02 = [(0, -1), (0, 0), (1, 0), (1, 1)]

tee01 = [(-1, 0), (0, 0), (1, 0), (0, 1)]
tee02 = [(-1, 0), (0, 0), (0, -1), (0, 1)]
tee03 = [(-1, 0), (0, 0), (0, -1), (1, 0)]
tee04 = [(0, 1), (0, 0), (0, -1), (1, 0)]

ai01 = [(-1, 0), (-0, 0), (1, 0), (2, 0)]
ai02 = [(0, -2), (0, -1), (0, 0), (0, 1)]

box = {"piece": [box01],
       "color": 1
       }
el = {"piece": [el01, el02, el03, el04],
      "color": 2
      }
jay = {"piece": [jay01, jay02, jay03, jay04],
       "color": 3
       }
zee = {"piece": [zee01, zee02],
       "color": 4
       }
ess = {"piece": [ess01, ess02],
       "color": 5
       }
tee = {"piece": [tee01, tee02, tee03, tee04],
       "color": 6
       }
ai = {"piece": [ai01, ai02],
      "color": 7
      }

pieces = [box, el, jay, zee, ess, tee, ai]

font_size = 2
jamma_font_short = pg.font.Font("font/jamma_short.ttf", (8*font_size))
jamma_font_tall = pg.font.Font("font/jamma_tall.ttf", (13*font_size))

text_next_white = surface_text_shadow("Next", (255,255,255), tall=False)
text_next_white_rect = text_next_white.get_rect()
text_next_white_rect.x = next_piece_posx - 24
text_next_white_rect.y = next_piece_posy - 40

text_title_white = surface_text_shadow("BichiTetris", (255,255,255), tall=True)
text_title_white_rect = text_title_white.get_rect()
text_title_white_rect.x = board_posx + 200
text_title_white_rect.y = board_posy - 60

background = pg.image.load("img/background01.png").convert()
background_rect = background.get_rect()

title = pg.image.load("img/title.png").convert_alpha()
title_rect = title.get_rect()

game_over_surf = pg.image.load("img/game_over.png").convert_alpha()
game_over_rect = game_over_surf.get_rect()

press_space = surface_text_shadow("Press SPACE BAR to start", (230, 230, 12), tall=False)
press_space_rect = press_space.get_rect()
press_space_rect.x = (screen.get_width() / 2)-(press_space_rect.w / 2)
press_space_rect.y = 430
press_space_show = False

instructions = [
    ("Move:   LEFT, RIGHT", white, False),
    #("LEFT and RIGHT.", white, False),
    (" ", white, False),
    ("Push:   DOWN", white, False),
    (" ", white, False),
    ("Rotate: UP", white, False),
    (" ", white, False),
    ("Screen: F", white, False),
    ("Exit:   ESC", white, False)]

instructions = surface_text_box(instructions)
instructions_rect = instructions.get_rect()
instructions_rect.x = (screen.get_width() / 2) - (instructions_rect.w / 2)
instructions_rect.y = (screen.get_height() / 2) - (instructions_rect.h / 2)

grey = 128,128,128

credits = [
    ("     Made with love for:", white, False),
    ("       Raquel & Ester", (255,0,0), True),
    (" ", white, False),
    ("          Music by:", white, False),
    ("https://chrislsound.itch.io/", (12,135,230), False),
    (" ", white, False),
    ("           Gfx by:", white, False),
    ("https://mattwalkden.itch.io/", (12,135,230), False),                      
]
credits =surface_text_box(credits)
credits_rect = credits.get_rect()
credits_rect.x = (screen.get_width() / 2) - (credits_rect.w / 2)
credits_rect.y = (screen.get_height() / 2) - (credits_rect.h / 2)

atract_screens = [(title, title_rect), (credits, credits_rect), (instructions, instructions_rect)]

PIECE_FALL = pg.event.custom_type()
PIECE_HIT = pg.event.custom_type()
GAME_OVER = pg.event.custom_type()
LEVEL_UP = pg.event.custom_type()
GAME_START = pg.event.custom_type()
GAME_ATRACT = pg.event.custom_type()
TEXT_BLINK = pg.event.custom_type()
SCREEN_CHANGE = pg.event.custom_type()

any_piece = random_piece()
current_piece = any_piece["piece"]
current_piece_color = any_piece["color"]

any_piece = random_piece()
next_piece = any_piece["piece"]
next_piece_color = any_piece["color"]

lines = 0
#text_lines_white = jamma_font_short.render(
#    "Lines", False, white).convert_alpha()
text_lines_white = surface_text_shadow("Lines", white, tall=False)
text_lines_white_rect = text_lines_white.get_rect()
text_lines_white_rect.x = lines_piece_posx - 24
text_lines_white_rect.y = lines_piece_posy - 40

text_number_white = None
text_number_white_rect = None
update_lines_text()

start_speed = 1000
speed = start_speed

sound_line1 = pg.mixer.Sound(file="snd/1line.wav")
sound_line2 = pg.mixer.Sound(file="snd/2lines.wav")
sound_line3 = pg.mixer.Sound(file="snd/3lines.wav")
sound_line4 = pg.mixer.Sound(file="snd/4lines.wav")

sound_hit = pg.mixer.Sound(file="snd/hit.wav")


"""
   _____ _             _   
  / ____| |           | |  
 | (___ | |_ __ _ _ __| |_ 
  \___ \| __/ _` | '__| __|
  ____) | || (_| | |  | |_ 
 |_____/ \__\__,_|_|   \__|
                           
                            """

pg.event.post(pg.event.Event(GAME_ATRACT, {}))

while not done:
    if game_status == "ATRACT":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # sys.exit()
                done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                pg.event.post(pg.event.Event(GAME_START, {}))
            if event.type == pg.KEYDOWN and event.key == pg.K_1:
                change_background(1)
            if event.type == pg.KEYDOWN and event.key == pg.K_2:
                change_background(2)
            if event.type == pg.KEYDOWN and event.key == pg.K_3:
                change_background(3)
            if event.type == pg.KEYDOWN and event.key == pg.K_4:
                change_background(4)
            if event.type == pg.KEYDOWN and event.key == pg.K_5:
                change_background(5)
            if event.type == pg.KEYDOWN and event.key == pg.K_6:
                change_background(6)
            if event.type == pg.KEYDOWN and event.key == pg.K_7:
                change_background(7)
            if event.type == pg.KEYDOWN and event.key == pg.K_8:
                change_background(8)
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                pg.display.toggle_fullscreen()
            if event.type == GAME_ATRACT:
                pg.time.set_timer(TEXT_BLINK, 2000)
                pg.time.set_timer(SCREEN_CHANGE, 7000)
                pg.mixer.music.load(filename="snd/start.ogg")
                pg.mixer.music.play(loops=0)
            if event.type == TEXT_BLINK:
                press_space_show = not press_space_show
            if event.type == SCREEN_CHANGE:
                element = atract_screens.pop()
                atract_screens.insert(0, element)
            if event.type == GAME_START:
                game_status = "GAME"
                reset_game()
                pg.time.set_timer(TEXT_BLINK, 0)
                pg.time.set_timer(SCREEN_CHANGE, 0)
                piece_pos_row = piece_pos_row_start
                piece_pos_col = piece_pos_col_start
                piece_rotation = 0
                get_next_piece()
                get_next_piece()
                break
        screen.blit(background, background_rect)
        blit_board()
        blit_text_next()
        blit_text_lines()
        screen.blit(text_number_white, text_number_white_rect)
        #screen.blit(title, title_rect)
        #screen.blit(instructions, instructions_rect)
        screen.blit(atract_screens[0][0], atract_screens[0][1])
        if press_space_show:
            screen.blit(press_space, press_space_rect)
        pg.display.flip()
        pg.time.Clock().tick(10)
    if game_status == "GAME":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # sys.exit()
                done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.event.clear()
                pg.event.post(pg.event.Event(GAME_OVER, {}))
                break
            if event.type == pg.KEYUP and event.key == pg.K_LEFT:
                move_piece_left(current_piece[piece_rotation])
            if event.type == pg.KEYUP and event.key == pg.K_RIGHT:
                move_piece_right(current_piece[piece_rotation])
            if event.type == pg.KEYUP and event.key == pg.K_DOWN:
                move_piece_down(current_piece[piece_rotation])
                pg.event.clear()
            if event.type == pg.KEYUP and event.key == pg.K_UP:
                move_piece_rotate_cw(current_piece)
                pg.event.clear()
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                pg.display.toggle_fullscreen()
            if event.type == PIECE_FALL:
                move_piece_down(current_piece[piece_rotation])
            if event.type == PIECE_HIT:
                pg.time.set_timer(PIECE_FALL, 0)
                copy_piece_to_board(
                    current_piece[piece_rotation], current_piece_color, piece_pos_row, piece_pos_col)
                piece_pos_row = piece_pos_row_start
                piece_pos_col = piece_pos_col_start
                piece_rotation = 0
                get_next_piece()
                delete_full_rows()
                set_level()
                pg.event.clear()
                if is_piece_occupied(current_piece[piece_rotation], piece_pos_row, piece_pos_col):
                    pg.event.post(pg.event.Event(GAME_OVER, {}))
                else:
                    pg.time.set_timer(PIECE_FALL, speed)
            if event.type == GAME_OVER:
                game_status = "GAME_OVER"
                pg.time.set_timer(PIECE_FALL, 0)
                pg.event.clear()
                pg.time.set_timer(GAME_ATRACT, 10000) # we change to Game Atract in 10 seconds
                pg.mixer.music.load(filename="snd/end.ogg")
                pg.mixer.music.play(loops=0)
                break
        # screen.fill(black)
        screen.blit(background, background_rect)

        blit_board()
        blit_piece(current_piece[piece_rotation],
                   current_piece_color, piece_pos_row, piece_pos_col)
        blit_next_piece(next_piece[0], next_piece_color)

        blit_text_next()
        blit_text_lines()
        screen.blit(text_number_white, text_number_white_rect)
        screen.blit(text_title_white, text_title_white_rect)
        pg.display.flip()
        pg.time.Clock().tick(60)
    if game_status == "GAME_OVER":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # sys.exit()
                done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                pg.display.toggle_fullscreen()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                pg.time.set_timer(GAME_ATRACT, 0)
                pg.event.post(pg.event.Event(GAME_ATRACT, {}))
                break
            if event.type == GAME_ATRACT:
                game_status = "ATRACT"
                pg.time.set_timer(PIECE_FALL, 0)
                pg.time.set_timer(GAME_ATRACT, 0)
                pg.event.clear()
                pg.event.post(pg.event.Event(GAME_ATRACT, {}))
                break
        screen.blit(background, background_rect)
        blit_board()
        blit_text_next()
        blit_text_lines()
        screen.blit(text_number_white, text_number_white_rect)
        screen.blit(text_title_white, text_title_white_rect)
        screen.blit(game_over_surf, game_over_rect)
        pg.display.flip()
        pg.time.Clock().tick(10)

pg.quit()
sys.exit()

# pyinstaller.exe --add-data="README.md;." --add-data="img;img" --add-data="snd;snd" --add-data="font;font" --icon=bichitetris.ico -w .\bichitetris.py
