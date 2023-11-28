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

# Function to handle mouse clicks
def mouse(button, state, x, y):
    global paused
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        normalized_x = (x / WINDOW_WIDTH) * 2 - 1
        normalized_y = ((WINDOW_HEIGHT - y) / WINDOW_HEIGHT) * 2 - 1
        
        # Check for button clicks based on normalized coordinates
        if -0.1 <= normalized_x <= 0.0 and 0.8 <= normalized_y <= 0.9:
            paused = not paused
            print("Pause clicked")
        elif -0.7 <= normalized_x <= -0.6 and 0.8 <= normalized_y <= 0.9:
            global diamonds, score, diamond_fall_speed, game_over
            if not paused:
                game_over = False
                diamonds = []
                score = 0
                diamond_fall_speed = 0.0001
                generate_diamond()
                print("Starting Over!!")
        elif 0.5 <= normalized_x <= 0.6 and 0.8 <= normalized_y <= 0.9:
            glutLeaveMainLoop()

# Function to close the window
def close_window():
    glutLeaveMainLoop()

DIAMOND_SIZE = 0.03  
diamonds = []  
diamond_fall_speed = 0.0001  
game_over = False

# Function to generate a new diamond
def generate_diamond():
    global  game_over
    if not game_over:
        x = random.uniform(-1.0, 1.0)
        y = 1.0 
        diamonds.append((x, y))
    else:
        diamonds.clear() 

# Function to update the position of diamonds
def update_diamonds():
    global diamond_fall_speed, game_over
    if not paused: 
        for i in range(len(diamonds)):
            x, y = diamonds[i]
            y -= diamond_fall_speed 
            diamonds[i] = (x, y)
            if y < -1.0:
                diamonds.pop(i)
                game_over = True 
                print("Game Over!!! Score: ", score)
                generate_diamond()  

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
