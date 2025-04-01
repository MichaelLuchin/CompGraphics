import math

widh = 2400
high = 1350
coef = 0.17

def bari(x0, y0, x1, y1, x2, y2, x, y):
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda2 = 1.0 - lambda0 - lambda1
    return lambda0, lambda1, lambda2

def draw_tr(img_mat, z_buff, color, texture_coords, texture_nums, texture, x0, y0, z0, x1, y1, z1, x2, y2, z2,  i0, i1, i2):
    a = 10000 * coef
    px0, py0 = a * x0 / z0 + widh / 2, a * y0 / z0 + high / 2
    px1, py1 = a * x1 / z1 + widh / 2, a * y1 / z1 + high / 2
    px2, py2 = a * x2 / z2 + widh / 2, a * y2 / z2 + high / 2

    I0 = i0[2]
    I1 = i1[2]
    I2 = i2[2]

    xmin = min(px0, px1, px2)
    xmax = max(px0, px1, px2)
    ymin = min(py0, py1, py2)
    ymax = max(py0, py1, py2)
    if (xmin < 0): xmin = 0
    if (ymin < 0): ymin = 0
    if (xmax > widh): xmax = widh
    if (ymax > high): ymax = high

    xmax = math.ceil(xmax)
    ymax = math.ceil(ymax)
    xmin = math.floor(xmin)
    ymin = math.floor(ymin)

    for x in range (xmin, xmax):
        for y in range (ymin, ymax):
            l0, l1, l2 = bari(px0,py0,px1,py1,px2,py2, x, y)
            if (l0 >= 0 and l1>= 0 and l2 >= 0):
                z_cord = l0*z0 + l1*z1 + l2*z2
                if z_cord > z_buff[y][x]:
                    continue
                else:
                    color = l0*I0+l1*I1+l2*I2
                    color *=-255
                    img_mat[y][x] = color
                    z_buff[y][x] = z_cord