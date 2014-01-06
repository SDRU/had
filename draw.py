
from pyglet.text import Label
from pyglet import gl      
        
def draw_rectangle(x1, y1, x2, y2):
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
    gl.glVertex2f(int(x1), int(y1))  # souradnice A
    gl.glVertex2f(int(x1), int(y2))  # souradnice B
    gl.glVertex2f(int(x2), int(y2))  # souradnice C, nakresli trojuhelnik ABC
    gl.glVertex2f(int(x2), int(y1))  # souradnice D, nakresli trojuhelnik BCD
    # dalsi souradnice E by nakreslila trojuhelnik CDE, atd.
    gl.glEnd()  # ukonci kresleni trojuhelniku

def draw_text(text, x, y, position, font_size):
    score = Label(
        text,
        font_name='League Gothic',
        font_size=font_size,
        x=x, y=y, anchor_x=position)
    score.draw()
