import numpy as np

def normal(x0,y0,z0,x1,y1,z1,x2,y2,z2):
    v1=np.array([x1-x2,y1-y2,z1-z2])
    v2=np.array([x1-x0,y1-y0,z1-z0])
    return np.cross(v1,v2)

def cut_nofacial(x0,y0,z0,x1,y1,z1,x2,y2,z2):
    l=[0,0,1]
    n=normal(x0,y0,z0,x1,y1,z1,x2,y2,z2)
    return(np.dot(n,l)/
           (np.linalg.norm(n) * np.linalg.norm(l)))

def model_rotation(alpha=np.radians(0), beta=np.radians(0), gamma=np.radians(0)):
    Rx=np.array(
        [[1,0,0],
         [0, np.cos(alpha), np.sin(alpha)],
         [0, -np.sin(alpha), np.cos(alpha)]]
    )
    Ry=np.array(
        [[np.cos(beta),0,np.sin(beta)],
        [0, 1,0],
        [-np.sin(beta),0,np.cos(beta)]]
    )
    Rz=np.array(
        [[np.cos(gamma), np.sin(gamma),0],
        [-np.sin(gamma),np.cos(gamma),0],
        [0, 0, 1]]
    )
    return np.dot(Rx,np.dot(Ry,Rz))

def resize(vectorv, tx=0, ty=0, tz=0, alpha=np.radians(0), beta=np.radians(0), gamma=np.radians(0)):
    for i in vectorv:
        i[0],i[1],i[2] = np.dot(model_rotation(alpha,beta,gamma),[i[0], i[1], i[2]]) + [tx,ty,tz]
    return vectorv

def get_point_normals(vectorv, vectorf, normalsArr):
    for i in range(0, len(vectorf)):
        x0 = (vectorv[vectorf[i][0] - 1][0])
        y0 = (vectorv[vectorf[i][0] - 1][1])
        z0 = (vectorv[vectorf[i][0] - 1][2])
        x1 = (vectorv[vectorf[i][1] - 1][0])
        y1 = (vectorv[vectorf[i][1] - 1][1])
        z1 = (vectorv[vectorf[i][1] - 1][2])
        x2 = (vectorv[vectorf[i][2] - 1][0])
        y2 = (vectorv[vectorf[i][2] - 1][1])
        z2 = (vectorv[vectorf[i][2] - 1][2])

        norm = normal(x0, y0, z0, x1, y1, z1, x2, y2, z2)
        norm /= np.linalg.norm(norm)
        normalsArr[vectorf[i][0] - 1] += norm
        normalsArr[vectorf[i][1] - 1] += norm
        normalsArr[vectorf[i][2] - 1] += norm
    for i in range(0, len(normalsArr)):
        normalsArr[i] = normalsArr[i]/np.linalg.norm(normalsArr[i])

    return normalsArr