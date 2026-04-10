import math
import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure

from utils.emiters import calculate_emitter_coordinates
from utils.bresenham import get_bresenham_pixels

def add_ray_trace(brightness, pixels, output_img_matrix, ray_counter_matrix, matrix_shape):
    for pixel_cords in pixels:
        if pixel_cords[0] >= 0 and pixel_cords[0] < matrix_shape[1] and pixel_cords[1] >= 0 and pixel_cords[1] < matrix_shape[0]:
            output_img_matrix[pixel_cords[1]][pixel_cords[0]] += brightness
            ray_counter_matrix[pixel_cords[1]][pixel_cords[0]] += 1

def show_image(output_img_matrix):
    plt.imshow(output_img_matrix, cmap='gray')
    plt.axis('off')
    plt.show()

def reconstruct_image(angle_coverage, img_matrix, N_detectors, l, N_scans, sinogram, rescale):
    angle = 0
    sinogram_row_counter = 0

    img_height, img_width = img_matrix.shape
    output_img_matrix = [[0 for _ in range(img_width)] for _ in range(img_height)]
    ray_counter_matrix = [[0 for _ in range(img_width)] for _ in range(img_height)]

    distance_between_emiters = l/N_detectors

    while angle <= angle_coverage:
        #głowica w nowej pozycji
        radius = math.sqrt(pow(img_width,2)+pow(img_height, 2))/2

        emiters_cords = calculate_emitter_coordinates(angle, N_detectors, distance_between_emiters, radius, img_matrix.shape)
        detectors_cords = calculate_emitter_coordinates(angle+180, N_detectors, distance_between_emiters, radius, img_matrix.shape)[::-1]
        
        for i in range(N_detectors):
            bresenham_pixels = get_bresenham_pixels(emiters_cords[i][0], emiters_cords[i][1], detectors_cords[i][0], detectors_cords[i][1])
            add_ray_trace(sinogram[sinogram_row_counter][i], bresenham_pixels, output_img_matrix, ray_counter_matrix, img_matrix.shape)
        
        angle += angle_coverage/N_scans
        sinogram_row_counter += 1


    #normalizacja
    for y in range(img_height):
        for x in range(img_width):
            if ray_counter_matrix[y][x] != 0:
                output_img_matrix[y][x] = output_img_matrix[y][x]/ray_counter_matrix[y][x]

    p_low, p_high = np.percentile(output_img_matrix, (50, 98))
    output_array = np.array(output_img_matrix)

    if rescale:
        rescaled_img = exposure.rescale_intensity(output_array, in_range=(p_low, p_high), out_range=(0, 1))
        return rescaled_img
        
    return output_array


