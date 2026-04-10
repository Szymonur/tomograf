def filter_sum_nornmalize(pixels, img_matrix):
    sum = 0
    for pixel_cords in pixels:
        if pixel_cords[0] >= 0 and pixel_cords[0] < img_matrix.shape[1] and pixel_cords[1] >= 0 and pixel_cords[1] < img_matrix.shape[0]:
            sum += img_matrix[pixel_cords[1]][pixel_cords[0]]
            #do potencjalnej alternatywnej normalizacji
    if len(pixels) == 0:
        return 0
    return sum / len(pixels)