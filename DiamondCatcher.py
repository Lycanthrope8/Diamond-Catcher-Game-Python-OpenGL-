from OpenGL.GL import *
from OpenGL.GLUT import *
import random

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 600

# Function to draw the back button
def draw_back_button():
    glColor3f(0.0, 1.0, 0.0)  
    glBegin(GL_LINES)
    glVertex2f(-0.7, 0.85) 
    glVertex2f(-0.6, 0.9)
    glVertex2f(-0.7, 0.85)  
    glVertex2f(-0.6, 0.8)
    glEnd()

# Function to draw the pause button
def draw_pause_button():
    glColor3f(1.0, 1.0, 0.0)  
    glBegin(GL_LINES)
    glVertex2f(-0.1, 0.9)
    glVertex2f(-0.1, 0.8)
    glVertex2f(0.0, 0.9)
    glVertex2f(0.0, 0.8)
    glEnd()

# Function to draw the cross button
def draw_cross_button():
    glColor3f(1.0, 0.0, 0.0)  
    glBegin(GL_LINES)
    glVertex2f(0.5, 0.9)
    glVertex2f(0.6, 0.8)
    glVertex2f(0.5, 0.8)
    glVertex2f(0.6, 0.9)
    glEnd()

CATCHER_WIDTH = 0.4 
catcher_position = 0.0  

# Function to draw the catcher using midpoint line algorithm
def draw_catcher():
    global game_over
    if game_over:
        glColor3f(1.0, 0.0, 0.0)  
    else:
        glColor3f(0.0, 0.0, 1.0)
    glLineWidth(2)  
    glBegin(GL_LINES)

    glVertex2f(catcher_position - CATCHER_WIDTH / 2, -0.85)  
    glVertex2f(catcher_position + CATCHER_WIDTH / 2, -0.85)  
    
    glVertex2f(catcher_position - CATCHER_WIDTH / 4, -0.9)  
    glVertex2f(catcher_position + CATCHER_WIDTH / 4, -0.9)  
    
    glVertex2f(catcher_position - CATCHER_WIDTH / 2, -0.85) 
    glVertex2f(catcher_position - CATCHER_WIDTH / 4, -0.9)  
    glVertex2f(catcher_position + CATCHER_WIDTH / 2, -0.85)
    glVertex2f(catcher_position + CATCHER_WIDTH / 4, -0.9) 
    glEnd()

# Function to handle special keys
def special_keys(key, x, y):
    global catcher_position, paused
    
    if not paused:
        if key == GLUT_KEY_LEFT:
            catcher_position -= 0.05
            if catcher_position < -1.0 + CATCHER_WIDTH / 2:
                catcher_position = -1.0 + CATCHER_WIDTH / 2
       
        elif key == GLUT_KEY_RIGHT:
            catcher_position += 0.05
            if catcher_position > 1.0 - CATCHER_WIDTH / 2:
                catcher_position = 1.0 - CATCHER_WIDTH / 2
    glutPostRedisplay()

paused = False  

# Function to draw the diamonds
def draw_diamonds():
    glColor3f(1.0, 1.0, 0.0)  
    for x, y in diamonds:
        glBegin(GL_LINES)
        glVertex2f(x, y)  
        glVertex2f(x - DIAMOND_SIZE, y - DIAMOND_SIZE)  
        glVertex2f(x, y)  
        glVertex2f(x + DIAMOND_SIZE, y - DIAMOND_SIZE) 
        glVertex2f(x - DIAMOND_SIZE, y - DIAMOND_SIZE)
        glVertex2f(x, y - 2 * DIAMOND_SIZE)  
        glVertex2f(x + DIAMOND_SIZE, y - DIAMOND_SIZE)  
        glVertex2f(x, y - 2 * DIAMOND_SIZE)  
        glEnd()

score = 0

# Function to check collision between catcher and diamonds
def check_collision(catcher_x, catcher_y, diamond_x, diamond_y):
    global score, diamond_fall_speed
    catcher_top = catcher_y + 0.05  
    if catcher_x - CATCHER_WIDTH / 2 <= diamond_x <= catcher_x + CATCHER_WIDTH / 2 and catcher_y <= diamond_y <= catcher_top:
        score += 1
        print("Score:", score)
        diamonds.remove((diamond_x, diamond_y))  
        generate_diamond()  
        diamond_fall_speed += 0.00002
    
# Main draw function
def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_back_button()
    draw_pause_button()
    draw_cross_button()
    draw_catcher()
    draw_diamonds()
    catcher_y = -0.875 
    for x, y in diamonds:
        check_collision(catcher_position, catcher_y, x, y)
    glutSwapBuffers()
    update_diamonds()
    glutPostRedisplay()

# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Diamond Catcher")
    glutDisplayFunc(draw)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse)
    glutCloseFunc(close_window)
    generate_diamond()
    glutMainLoop()

if __name__ == "__main__":
    main()
