import math

from PIL import  Image, ImageOps
import CompGraphics as gc

def bari(x0, y0, x1, y1, x2, y2, x, y):
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda2 = 1.0 - lambda0 - lambda1
    return lambda0, lambda1, lambda2

def draw_tr(x0, y0, z0, x1, y1, z1, x2, y2, z2, img_mat, z_buff, color):
    xmin = min(x0, x1, x2)
    xmax = max(x0, x1, x2)
    ymin = min(y0, y1, y2)
    ymax = max(y0, y1, y2)
    if (xmin < 0): xmin = 0
    if (ymin < 0): ymin = 0

    xmax = math.ceil(xmax)
    ymax = math.ceil(ymax)
    xmin = math.floor(xmin)
    ymin = math.floor(ymin)

    for x in range (xmin, xmax):
        for y in range (ymin, ymax):
            l0, l1, l2 = bari(x0, y0, x1, y1, x2, y2, x, y)
            if (l0 >= 0 and l1>= 0 and l2 >= 0):
                z_cord = l0*z0 + l1*z1 + l2*z2
                if z_cord > z_buff[y][x]:
                    continue
                else:
                    img_mat[y, x] = color
                    z_buff[y][x] = z_cord

# img_mat2 = np.zeros(shape=(2000, 2000, 3), dtype=np.uint8)
# draw_tr(50.0, 50.0, 1000.0, 1000.0, 50.0, 1500.0, img_mat2)
# img = Image.fromarray(img_mat2, mode="RGB")
# img = ImageOps.flip(img)
# img.save("img.jpg")