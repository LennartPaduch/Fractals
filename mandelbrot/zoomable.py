import pygame as pg
import numpy as np
import numba
import math

pg.init()

windowSize = width, height = 1280, 960
screen = pg.display.set_mode(windowSize)
x1, x2, y1, y2 = -2.0, 1.0, -1.0, 1.0
maxIt = 1024
fractal = np.zeros((width, height, 3), dtype=np.uint8)
clock = pg.time.Clock()


def update_scale(width, height, x1, x2, y1, y2):
    return width / (x2 - x1), height / (y2 - y1)

scale_x, scale_y = update_scale(width, height, x1, x2, y1, y2)

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
            if i < maxIt:
                r = int((0.5 * math.sin(0.1 * i + 0) + 0.5) * 255)  
                g = int((0.5 * math.sin(0.1 * i + 2) + 0.5) * 255)  
                b = int((0.5 * math.sin(0.1 * i + 4) + 0.5) * 255) 
                fractal[x, y] = (r, g, b)
            else:
                fractal[x, y] = (0, 0, 0)

dragging = False
last_mouse_pos = None

while True:
    clock.tick()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                last_mouse_pos = event.pos
            elif event.button == 4:  # Mouse wheel up
                zoom_factor = 0.9
                mx, my = pg.mouse.get_pos()
                x1, x2 = x1 + (mx / scale_x) * (1 - zoom_factor), x2 - ((width - mx) / scale_x) * (1 - zoom_factor)
                y1, y2 = y1 + (my / scale_y) * (1 - zoom_factor), y2 - ((height - my) / scale_y) * (1 - zoom_factor)
            elif event.button == 5:  # Mouse wheel down
                zoom_factor = 1.1
                mx, my = pg.mouse.get_pos()
                x1, x2 = x1 + (mx / scale_x) * (1 - zoom_factor), x2 - ((width - mx) / scale_x) * (1 - zoom_factor)
                y1, y2 = y1 + (my / scale_y) * (1 - zoom_factor), y2 - ((height - my) / scale_y) * (1 - zoom_factor)
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        elif event.type == pg.MOUSEMOTION:
            if dragging:
                dx, dy = event.pos[0] - last_mouse_pos[0], event.pos[1] - last_mouse_pos[1]
                x1, x2 = x1 - dx / scale_x, x2 - dx / scale_x
                y1, y2 = y1 - dy / scale_y, y2 - dy / scale_y
                last_mouse_pos = event.pos

    scale_x, scale_y = update_scale(width, height, x1, x2, y1, y2)

    draw(width, height, x1, y1, scale_x, scale_y, maxIt, fractal)
    pg.surfarray.blit_array(screen, fractal)
    pg.display.flip()
    pg.display.set_caption(f'FPS = {clock.get_fps():.2f}')
