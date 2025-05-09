import numpy as np

def dotted_line(image, x0, y0, x1, y1, color):
    count = np.sqrt((x1-x0)**2 + (y1-y0)**2)
    step = 1.0/count
    for t in np.arange (0,1, step):
        x = round ((1.0 - t ) *x0 + t*x1)
        y = round ((1.0 - t ) * y0 + t*y1)
        image[y, x] = color

def x_loop_line(image, x0, y0, x1, y1, color):
    xchange = False

    if (abs(x0 - x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True

    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    for x in np.arange(x0, x1):
        t = (x-x0)/(x1 - x0)
        y = round ((1.0 - t) * y0 + t*y1)
        if (xchange):
            image[x, y] = color
        else:
            image[y, x] = color

def bresanham(image, x0, y0, x1, y1, color):
    xchange = False

    if (abs(x0 - x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True

    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    y = y0
    dy = abs(y1-y0)*2
    derror = 0.0 #Смещение по у
    y_update = 1 if y1 > y0 else -1

    for x in np.arange(x0, x1):
        if (xchange):
            image[x, y] = color
        else:
            image[y, x] = color

        derror += dy
        if (derror > (x1 - x0)):
            derror -= 2 * (x1 - x0)
            y += y_update
