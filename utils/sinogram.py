import numpy as np
import matplotlib.pyplot as plt
import math
from utils.emiters import calculate_emitter_coordinates
from utils.bresenham import get_bresenham_pixels
from utils.pixels_sum import filter_sum_nornmalize

def scan_generate_sinogram(N_detectors, distance_between_emitters, angle_coverage, N_scans, img_matrix):
    sinogram = []
    angle = 0
    img_height, img_width = img_matrix.shape
    radius = math.sqrt(pow(img_width,2)+pow(img_height, 2))/2

    while angle <= angle_coverage:
        #głowica w nowej pozycji

        emiters_cords = calculate_emitter_coordinates(angle, N_detectors, distance_between_emitters, radius, img_matrix.shape)
        detectors_cords = calculate_emitter_coordinates(angle+180, N_detectors, distance_between_emitters, radius, img_matrix.shape)[::-1]
        
        sinogram_row = []
        for i in range(N_detectors):
            bresenham_pixels = get_bresenham_pixels(emiters_cords[i][0], emiters_cords[i][1], detectors_cords[i][0], detectors_cords[i][1])
            sinogram_row.append(filter_sum_nornmalize(bresenham_pixels, img_matrix))
        sinogram.append(sinogram_row)
        angle += angle_coverage/N_scans

    return sinogram


def show_sinogram(sinogram_matrix):
    sinogram_np = np.array(sinogram_matrix)
    h, w = sinogram_np.shape
    target_width = 6
    target_height = target_width * (h / w)
    plt.figure(figsize=(target_width, target_height))
    plt.imshow(sinogram_np, cmap='gray', aspect='auto')

    plt.xlabel("Indeks detektora")
    plt.ylabel("Indeks skanu (Kąt)")
    plt.title("Sinogram")
    plt.colorbar()
    plt.show()