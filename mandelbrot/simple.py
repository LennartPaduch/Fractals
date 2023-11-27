import pygame as pg
from time import perf_counter as clock

# Initialize Pygame
pg.init()

windowSize = width, height = 1280, 960
screen = pg.display.set_mode(windowSize)
x1, x2, y1, y2 = -2.0, 1.0, -1.0, 1.0
maxIt = 30
scale_x = width / (x2 - x1)
scale_y = height / (y2 - y1)

def mandelbrot(c):
    z = 0
    for i in range(maxIt):
        if abs(z) > 2.0:
            break
        z = z**2 + c
    return i

def draw():
    for x in range(width):
        for y in range(height):
            c = complex(x / scale_x + x1, y / scale_y + y1) 
            i = mandelbrot(c)
            color = 255 / maxIt * i
            screen.set_at((x, y), (color, color, color))

start = clock()
draw() 
pg.display.flip()  
print(clock() - start)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            break  


