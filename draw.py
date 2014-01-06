from pyglet import gl      
        
def draw_rectangle(x1, y1, x2, y2,piece):
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
    gl.glVertex2f(int(x1)*piece, int(y1)*piece)  # souradnice A
    gl.glVertex2f(int(x1)*piece, int(y2)*piece)  # souradnice B
    gl.glVertex2f(int(x2)*piece, int(y2)*piece)  # souradnice C, nakresli trojuhelnik ABC
    gl.glVertex2f(int(x2)*piece, int(y1)*piece)  # souradnice D, nakresli trojuhelnik BCD
    # dalsi souradnice E by nakreslila trojuhelnik CDE, atd.
    gl.glEnd()  # ukonci kresleni trojuhelniku
