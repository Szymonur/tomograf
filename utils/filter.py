import math
import numpy as np

def filter_sinogram(sinogram):
    filter = []
    for k in range(-10,11):
        if k == 0:
            filter.append(1)
        elif k%2 == 0:
            filter.append(0)
        else:
            filter.append(-4/pow(math.pi,2)/pow(k,2))

    filtered_sinogram = []

    for i in range(len(sinogram)):
        filtered_sinogram.append(np.convolve(sinogram[i], filter, mode='same'))

    return filtered_sinogram