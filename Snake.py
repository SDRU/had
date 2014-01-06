import sys
from time import sleep
from random import randint

import pyglet
from pyglet import gl
from pyglet.window import key

from draw import draw_rectangle, draw_text


if len(sys.argv) == 2:
    PIECE = int(sys.argv[1])
else:
    PIECE = 10

### Snake consists of N pieces 10*10

### Units - snake pieces
WIDTH=100
HEIGHT=50
SNAKE_LENGTH=20
N=20
WALL_THICKNESS=1
FONT_SIZE=4
SCORE_POSITION=[WIDTH//2-FONT_SIZE//2,HEIGHT-FONT_SIZE-WALL_THICKNESS]
QUIT_SIGNAL=0

speed = 0.1  # s
elapsed_time = 0

snake_position = []
food_position=(WIDTH//2, HEIGHT//2)

last_key='right'

DIRECTIONS = {
     'up': (0, 1),
     'down': (0, -1),
     'left': (-1, 0),
     'right': (1, 0)
}
                 
def reset():
    global N, last_key, snake_position, food_position
    N=20
    snake_position = []

    for i in range(0, N):
        snake_position.append((WIDTH//2+i, HEIGHT//2))

    last_key = 'right' # Default movement of snake is right direction
    food_position = (randint(WALL_THICKNESS + 1, WIDTH - WALL_THICKNESS-1),
                     randint(WALL_THICKNESS + 1, HEIGHT-WALL_THICKNESS-1))
    ### Food is placed periodically with period PIECE

       
def refresh():
    global snake_position, last_key, N, QUIT_SIGNAL, food_position
    if QUIT_SIGNAL==1:
        return
    ### Last element of snake removed to the front, according to pressed key

    snake_position[:-1]=snake_position[1:]

    dx, dy = DIRECTIONS[last_key]
    snake_position[-1] = (snake_position[-1][0] + dx, snake_position[-1][1] + dy)

    ### Snake hits the boundary. QUIT_SIGNAL is activated    
    if (snake_position[-1][0] + 1 > WIDTH-WALL_THICKNESS or
            snake_position[-1][0] < WALL_THICKNESS or 
            snake_position[-1][1] + 1 > HEIGHT-WALL_THICKNESS or 
            snake_position[-1][1] < WALL_THICKNESS):
        QUIT_SIGNAL = 1

    ### Eating food
    if snake_position[-1] == food_position:
        snake_position.append((food_position[0] + dx, food_position[1] + dy))

        ### New food appears
        food_position = (randint(WALL_THICKNESS + 1, WIDTH - WALL_THICKNESS-1),
                     randint(WALL_THICKNESS + 1, HEIGHT-WALL_THICKNESS-1))
        N+=1

   ### Checks is snake doesn't cross itself, it is impossible to cross -2 element also
    if snake_position[-1] in snake_position[:-1]:
        QUIT_SIGNAL = 1

def drawing():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # smaz obsah okna (vybarvi na cerno)
    gl.glColor3f(0, 1, 0)  # nastav barvu kresleni na zelenu

    ### Plots the snake body
    for i in range(0,len(snake_position)-1):
        draw_rectangle(PIECE*snake_position[i][0],PIECE*snake_position[i][1],PIECE*(snake_position[i][0]+1),PIECE*(snake_position[i][1]+1))

    ### Snake head in blue
    gl.glColor3f(0, 0, 1)
    draw_rectangle(PIECE*snake_position[-1][0],PIECE*snake_position[-1][1],PIECE*(snake_position[-1][0]+1),PIECE*(snake_position[-1][1]+1))
    
    ### Food
    draw_rectangle(PIECE*food_position[0],PIECE*food_position[1],PIECE*(food_position[0]+1),PIECE*(food_position[1]+1))
    ### Score
    draw_text(str(N-20),PIECE*SCORE_POSITION[0],PIECE*SCORE_POSITION[1],'left', PIECE*FONT_SIZE)
    ### Walls
    gl.glColor3f(0, 1, 0)  # nastav barvu kresleni na zelenu   
    draw_rectangle(0, 0, PIECE*WALL_THICKNESS, PIECE*HEIGHT)
    draw_rectangle(0, 0, PIECE*WIDTH, PIECE*WALL_THICKNESS)
    draw_rectangle(PIECE*WIDTH-PIECE*WALL_THICKNESS,0,PIECE*WIDTH,PIECE*HEIGHT)
    draw_rectangle(0,PIECE*HEIGHT-PIECE*WALL_THICKNESS,PIECE*WIDTH,PIECE*HEIGHT)

    if QUIT_SIGNAL==1:
        draw_text('GAME OVER',PIECE*WIDTH//2-PIECE*FONT_SIZE*4,PIECE*HEIGHT//2-PIECE*FONT_SIZE//2,'left', PIECE*FONT_SIZE)


        
def key_press(symbol, modificators):
    
    """Osetri stisknuti klavesy

    Kdyz hrac stiskne spravnou klavesu, do mnoziny ``stisknute_klavesy`` se
    prida dvojice (n-tice) tvaru (smer, cislo palky).
    Program pak muze pohybovat palkou podle toho, co je v mnozine.
    """
    global last_key
    if symbol == key.LEFT and last_key != 'right':
        last_key = 'left'
    if symbol == key.RIGHT and last_key != 'left':
        last_key = 'right'
    if symbol == key.UP and last_key != 'down':
        last_key = 'up'
    if symbol == key.DOWN and last_key != 'up':
        last_key = 'down'
    # N.B. klavesu ESC Pyglet osetri sam: zavre okno a ukonci funkci run()

def update(dt):
    global elapsed_time
    elapsed_time += dt
    while elapsed_time > speed:
        elapsed_time-=speed
        refresh()

# Nastavime prvotni stav
reset()

# Vytvorime okno, do ktereho budeme kreslit
window = pyglet.window.Window(width=int(WIDTH*PIECE), height=int(HEIGHT*PIECE))

# Oknu priradime par funkci, ktere budou reagovat na udalosti.
# Kdyz napr. uzivatel zmackne klavesu na klavesnici,
# Pyglet zavola funkci, kterou tady zaregistrujeme pod `on_key_press`,
# a preda ji prislusne argumenty.
# Jake vsechny udalosti muzou nastat, a jake argumenty se predaji prislusne
# funkci, se doctete v dokumentaci Pygletu,
# nebo pomoci `help(pyglet.window.event)`.
window.push_handlers(
    on_draw=drawing,  # na vykresleni okna pouzij funkci `vykresli`
    on_key_press=key_press,  # po stisknuti klavesy zavolej `stisk_klavesy`
    )

# Jeste mame jednu podobnou funkci, kterou ale neprirazujeme primo
# oknu. Misto toho chceme aby ji Pyglet zavolal vzdycky kdyz "tiknou hodiny"


pyglet.clock.schedule(update) # Waits 0.1 s between another clock tick

pyglet.app.run()  # vse je nastaveno, at zacne hra
# (funkce run() bude porad dokola volat obnov_stav, vykresli, a kdyz se mezitim
# neco stane, zavola navic funkci kterou jsme nastavili jako reakci na
# danou udalost)
