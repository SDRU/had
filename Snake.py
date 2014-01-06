import pyglet
from pyglet import gl
from pyglet.window import key
import random
from random import choice
from time import sleep

### Snake consists of N pieces 10*10

global N, released, snake_position_x, snake_position_y, QUIT_SIGNAL, fps
### Units - snake pieces
WIDTH=100
HEIGHT=50
SNAKE_LENGTH=20
N=20
PIECE=SNAKE_LENGTH/N*10 # 1*10 px
WALL_THICKNESS=1
FONT_SIZE=4
SCORE_POSITION=[WIDTH//2-FONT_SIZE//2,HEIGHT-FONT_SIZE-WALL_THICKNESS]
QUIT_SIGNAL=0

snake_position_x=[0]*N
snake_position_y=[0]*N
released=[0,0,0,0]
food_position=[WIDTH//2,HEIGHT//2]
fps=10.0

for i in range(0,N):
    snake_position_x[i]=WIDTH//2+i
    snake_position_y[i]=HEIGHT//2
pressed_keys=set([])
                 

def reset():
    global N, released, snake_position_x, snake_position_y
    N=20
    food_position[0]=0
    food_position[1]=0
    for i in range(0,N):
        snake_position_x[i]=WIDTH//2+i
        snake_position_y[i]=HEIGHT//2
    released[0]=0
    released[1]=0
    released[2]=0
    released[3]=1 # Default movement of snake is right direction
    food_position[0]=choice([t for t in range(WALL_THICKNESS+1,WIDTH-1-WALL_THICKNESS-1)])
    food_position[1]=choice([t for t in range(WALL_THICKNESS+1,HEIGHT-1-WALL_THICKNESS-1)])
    ### Food is placed periodically with period PIECE

       
def refresh(dt):
    global snake_position_x, snake_position_y, released, N, QUIT_SIGNAL, fps
    ### Last element of snake removed to the front, according to pressed key
    ### Second if argument always prevents the snake to move if user presses the key of opposite direction
    if (('up') in pressed_keys) and released[1]==0:
        snake_position_x[:-1]=snake_position_x[1:]
        snake_position_y[:-1]=snake_position_y[1:]
        snake_position_y[-1]=snake_position_y[-1]+1
        released[0]=1
        released[1]=0
        released[2]=0
        released[3]=0

    if ('down') in pressed_keys and released[0]==0:
        snake_position_x[:-1]=snake_position_x[1:]
        snake_position_y[:-1]=snake_position_y[1:]
        snake_position_y[-1]=snake_position_y[-1]-1
        released[0]=0
        released[1]=1
        released[2]=0
        released[3]=0
        
    if ('left') in pressed_keys and released[3]==0:
        snake_position_x[:-1]=snake_position_x[1:]
        snake_position_y[:-1]=snake_position_y[1:]
        snake_position_x[-1]=snake_position_x[-1]-1
        released[0]=0
        released[1]=0
        released[2]=1
        released[3]=0
        
    if ('right') in pressed_keys and released[2]==0:
        snake_position_x[:-1]=snake_position_x[1:]
        snake_position_y[:-1]=snake_position_y[1:]
        snake_position_x[-1]=snake_position_x[-1]+1
        released[0]=0
        released[1]=0
        released[2]=0
        released[3]=1

    ### If nothing is pressed, snake continues the same direction
    if released[0]==1: # **************
        snake_position_x[:-1]=snake_position_x[1:]
        snake_position_y[:-1]=snake_position_y[1:]
        snake_position_y[-1]=snake_position_y[-1]+1

    if released[1]==1:
        snake_position_x[:-1]=snake_position_x[1:]
        snake_position_y[:-1]=snake_position_y[1:]
        snake_position_y[-1]=snake_position_y[-1]-1

    if released[2]==1:
        snake_position_x[:-1]=snake_position_x[1:]
        snake_position_y[:-1]=snake_position_y[1:]
        snake_position_x[-1]=snake_position_x[-1]-1
    
     
    if released[3]==1:
        snake_position_x[:-1]=snake_position_x[1:]
        snake_position_y[:-1]=snake_position_y[1:]
        snake_position_x[-1]=snake_position_x[-1]+1

    ### Snake hits the boundary. QUIT_SIGNAL is activated    
    if snake_position_x[-1]+1>WIDTH-WALL_THICKNESS or snake_position_x[-1]<WALL_THICKNESS or snake_position_y[-1]+1>HEIGHT-WALL_THICKNESS or snake_position_y[-1]<WALL_THICKNESS:
        QUIT_SIGNAL=1

    ### Eating food. Position of -1 snake element if equal to food position. Why also -2? If the snake suddenly changes direction one element distance before the food appears,
      # it is moved 2 square elements in the same direction - first because of key pressing, then it follows the direction to keep it moving, see ***********
    if (snake_position_x[-1]==food_position[0] and snake_position_y[-1]==food_position[1]) or (snake_position_x[-2]==food_position[0] and snake_position_y[-2]==food_position[1]):

        if released==[0,0,0,1]: # from left, right key is pressed
            snake_position_x.append(food_position[0]+1)
            snake_position_y.append(food_position[1])
            
        elif released==[0,1,0,0]: # from up, down key is pressed
            snake_position_x.append(food_position[0])
            snake_position_y.append(food_position[1]-1)

        elif released==[0,0,1,0]: # from right, left key is pressed
            snake_position_x.append(food_position[0]-1)
            snake_position_y.append(food_position[1])
            
        elif released==[1,0,0,0]: # from down, up key is pressed
            snake_position_x.append(food_position[0])
            snake_position_y.append(food_position[1]+1)

        ### New food appears
        food_position[0]=choice([t for t in range(0,WIDTH-1)])
        food_position[1]=choice([t for t in range(0,HEIGHT-1)])
        N+=1
##        fps+=0.001
##        print fps
##        pyglet.clock.schedule_interval(refresh,1/fps)

   ### Checks is snake doesn't cross itself, it is impossible to cross -2 element also
    indx = [i for i, x in enumerate(snake_position_x[:-2]) if x == snake_position_x[-1]] # List of all other snake positions with same x value as the last element
    indy = [i for i, y in enumerate(snake_position_y[:-2]) if y == snake_position_y[-1]] # List of all other snake positions (except last two) with same y value as the last element
    for i in indx: # indx and indy==True => Last element crosses with snake
        if i in indy:
            QUIT_SIGNAL=1
            
        
        
def draw_rectangle(x1, y1, x2, y2):
    global N, released, snake_position_x, snake_position_y

    """Nakresli obdelnik na dane souradnice

    Nazorny diagram::

         y2 - +-----+
              |/////|
         y1 - +-----+
              :     :
             x1    x2
    """
    # Tady pouzivam volani OpenGL, ktere je pro nas zatim asi nejjednodussi
    # na pouziti
    gl.glBegin(gl.GL_TRIANGLE_FAN)   # zacni kreslit spojene trojuhelniky
    gl.glVertex2f(int(x1)*PIECE, int(y1)*PIECE)  # souradnice A
    gl.glVertex2f(int(x1)*PIECE, int(y2)*PIECE)  # souradnice B
    gl.glVertex2f(int(x2)*PIECE, int(y2)*PIECE)  # souradnice C, nakresli trojuhelnik ABC
    gl.glVertex2f(int(x2)*PIECE, int(y1)*PIECE)  # souradnice D, nakresli trojuhelnik BCD
    # dalsi souradnice E by nakreslila trojuhelnik CDE, atd.
    gl.glEnd()  # ukonci kresleni trojuhelniku

def draw_text(text, x, y, position):
    score = pyglet.text.Label(
        text,
        font_name='League Gothic',
        font_size=FONT_SIZE*PIECE,
        x=x*PIECE, y=y*PIECE, anchor_x=position)
    score.draw()


def drawing():
    global QUIT_SIGNAL
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # smaz obsah okna (vybarvi na cerno)
    gl.glColor3f(0, 1, 0)  # nastav barvu kresleni na zelenu

    ### Plots the snake body
    for i in range(0,len(snake_position_x)-1):
        draw_rectangle(snake_position_x[i],snake_position_y[i],snake_position_x[i]+1,snake_position_y[i]+1)

    ### Snake head in blue
    gl.glColor3f(0, 0, 1)
    draw_rectangle(snake_position_x[-1],snake_position_y[-1],snake_position_x[-1]+1,snake_position_y[-1]+1)
    
    ### Food
    draw_rectangle(food_position[0],food_position[1],food_position[0]+1,food_position[1]+1)
    ### Score
    draw_text(str(N-20),SCORE_POSITION[0],SCORE_POSITION[1],'left')
    ### Walls
    gl.glColor3f(0, 1, 0)  # nastav barvu kresleni na zelenu   
    draw_rectangle(0,0,WALL_THICKNESS,HEIGHT)
    draw_rectangle(0,0,WIDTH,WALL_THICKNESS)
    draw_rectangle(WIDTH-WALL_THICKNESS,0,WIDTH,HEIGHT)
    draw_rectangle(0,HEIGHT-WALL_THICKNESS,WIDTH,HEIGHT)

    if QUIT_SIGNAL==1:
        draw_text('GAME OVER',WIDTH//2-FONT_SIZE*4,HEIGHT//2-FONT_SIZE//2,'left')
        pyglet.clock.unschedule(refresh) # Stops clock
        
        
        
def key_press(symbol, modificators):
    
    """Osetri stisknuti klavesy

    Kdyz hrac stiskne spravnou klavesu, do mnoziny ``stisknute_klavesy`` se
    prida dvojice (n-tice) tvaru (smer, cislo palky).
    Program pak muze pohybovat palkou podle toho, co je v mnozine.
    """
    if symbol == key.LEFT:
        pressed_keys.add('left')
    if symbol == key.RIGHT:
        pressed_keys.add('right')
    if symbol == key.UP:
        pressed_keys.add('up')
    if symbol == key.DOWN:
        pressed_keys.add('down')
    # N.B. klavesu ESC Pyglet osetri sam: zavre okno a ukonci funkci run()


def key_release(symbol, modificators):
    """Osetri pusteni klavesy

    Opak funkce ``stisk_klavesy`` -- podle argumentu vynda prislusnou
    dvojici z mnoziny.
    """
    # Vsimnete si pouziti funkce ``discard``: na rozdil od ``remove``
    # nezpusobi chybu, kdyz prvek v mnozine neni. Takze program nespadne,
    # kdyz napr. uzivatel zmackne klavesu, pak se prepne do naseho okna,
    # a pak teprve klavesu pusti.
    if symbol == key.LEFT:
        pressed_keys.discard('left')
    if symbol == key.RIGHT:
        pressed_keys.discard('right')
    if symbol == key.UP:
        pressed_keys.discard('up')
    if symbol == key.DOWN:
        pressed_keys.discard('down')
    # Mimochodem, funkce pusteni_klavesy a stisk_klavesy by se daly hodne
    # zjednodusit pomoci slovniku. Zkusite to?

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
    on_key_release=key_release,  # a mame i funkci na  pusteni klavesy
    )

# Jeste mame jednu podobnou funkci, kterou ale neprirazujeme primo
# oknu. Misto toho chceme aby ji Pyglet zavolal vzdycky kdyz "tiknou hodiny"


pyglet.clock.schedule_interval(refresh,1/fps) # Waits 0.1 s between another clock tick

pyglet.app.run()  # vse je nastaveno, at zacne hra
# (funkce run() bude porad dokola volat obnov_stav, vykresli, a kdyz se mezitim
# neco stane, zavola navic funkci kterou jsme nastavili jako reakci na
# danou udalost)
