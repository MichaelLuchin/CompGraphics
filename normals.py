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