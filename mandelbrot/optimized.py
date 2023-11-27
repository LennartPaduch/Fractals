import pygame as pg
import numpy as np
import numba

# Initialize Pygame
pg.init()

# Setting up the window and fractal parameters
windowSize = width, height = 1280, 960
screen = pg.display.set_mode(windowSize)
x1, x2, y1, y2 = -2.0, 1.0, -1.0, 1.0
maxIt = 30
scale_x = width / (x2 - x1)
scale_y = height / (y2 - y1)
fractal = np.zeros((width, height, 3), dtype=np.uint8)
clock = pg.time.Clock()

@numba.jit(nopython=True, fastmath=True, parallel=True)
def draw(width, height, x1, y1, scale_x, scale_y, maxIt, fractal):
    for x in numba.prange(width):
        for y in numba.prange(height):
            c = complex(x / scale_x + x1, y / scale_y + y1) 
            z = 0
            for i in range(maxIt):
                if z.real **2 + z.imag ** 2 > 4.0:
                    break
                z = z**2 + c
            color = 255 - int(255 * i / maxIt)
            fractal[x, y] = color, color, color

while True:
    clock.tick()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit() # Clean exit from the script
    draw(width, height, x1, y1, scale_x, scale_y, maxIt, fractal)
    pg.surfarray.blit_array(screen, fractal)
    pg.display.flip()
    pg.display.set_caption(f'FPS = {clock.get_fps():.2f}')
