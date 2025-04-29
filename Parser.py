import numpy as np
from PIL import  Image, ImageOps
import baricentric as bc
import normals as norm
import quaternions as quat

IMGTexture_exist = False
VTexture_exist = False
texture_img = None
try:
    texture_img = Image.open("12268_banjofrog_diffuse.jpg")
    IMGTexture_exist = True  # Успешно загружено
except Exception as e:
    print(f"Ошибка загрузки изображения: {e}")
    IMGTexture_exist = False

if IMGTexture_exist:
    texture = np.array(ImageOps.flip(texture_img))

img_mat2 = np.zeros(shape=(bc.high, bc.widh, 3), dtype=np.uint8)
z_buff_mat = np.full((bc.high, bc.widh), np.inf, dtype=np.float64)
for times in range (2):
    model = open("12268_banjofrog_v1_L3.obj")
    vectorv = []
    vectorf = []
    texture_coords = []
    texture_nums = []
    for line in model:
        v = line.split()
        if len(v) == 0:
            continue
        if (v[0] == "vt"):
            texture_coords.append([float(v[1]), float(v[2])])
            VTexture_exist = True
        if (v[0] == "v"):
            vectorv.append([float(v[1]), float(v[2]), float(v[3])])
        if (v[0] == "f"):
            for i in range(2, len(v) - 1):
                v1 = v[1].split('/')[0]
                v2 = v[i].split('/')[0]
                v3 = v[i+1].split('/')[0]
                th1 = v[1].split('/')[1]
                th2 = v[i].split('/')[1]
                th3 = v[i+1].split('/')[1]
                vectorf.append([int(v1), int(v2), int(v3)])
                texture_nums.append([int(th1), int(th2), int(th3)])


    #vectorv = norm.resize(vectorv,5 - 10*times, -0.1, 100*bc.coef,np.radians(150),np.radians(0),np.radians(210))
    vectorv = quat.transform_mesh(
        vectorv,
        translation=(-5 + 10*times, 0, 30),
        euler_angles=(np.radians(90), np.radians(100), np.radians(150)),
        scale=1
    )
    normalsArr = np.zeros((len(vectorv), 3))
    normalsArr = norm.get_point_normals(vectorv, vectorf, normalsArr)

    for i in range(0,len(vectorf)):
        x0 = (vectorv[vectorf[i][0]-1][0])
        y0 = (vectorv[vectorf[i][0]-1][1])
        z0 = (vectorv[vectorf[i][0]-1][2])
        x1 = (vectorv[vectorf[i][1]-1][0])
        y1 = (vectorv[vectorf[i][1]-1][1])
        z1 = (vectorv[vectorf[i][1]-1][2])
        x2 = (vectorv[vectorf[i][2]-1][0])
        y2 = (vectorv[vectorf[i][2]-1][1])
        z2 = (vectorv[vectorf[i][2]-1][2])

        polygon_texture_nums = texture_nums[i]

        light = norm.cut_nofacial(x0, y0, z0, x1, y1, z1, x2, y2, z2)
        color = (-255 * light,-255*light,-255*light)
        if (norm.cut_nofacial(x0, y0, z0, x1, y1, z1, x2, y2, z2) < 0):
            if IMGTexture_exist and VTexture_exist:
                bc.draw_tr_textured(img_mat2, z_buff_mat, polygon_texture_nums, texture_coords, texture, x0, y0, z0, x1, y1, z1, x2, y2, z2, normalsArr[vectorf[i][0] - 1], normalsArr[vectorf[i][1] - 1], normalsArr[vectorf[i][2] - 1])
            else:
                bc.draw_tr(img_mat2, z_buff_mat, x0, y0, z0, x1, y1, z1, x2, y2, z2, normalsArr[vectorf[i][0] - 1], normalsArr[vectorf[i][1] - 1], normalsArr[vectorf[i][2] - 1])

img = Image.fromarray(img_mat2, mode="RGB")
img = ImageOps.flip(img)
img.save("img.jpg")
