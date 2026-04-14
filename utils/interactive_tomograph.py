import numpy as np
import matplotlib.pyplot as plt
import math
import ipywidgets as widgets
from IPython.display import display
from skimage import exposure

# Importy z Twoich plików
from utils.emiters import calculate_emitter_coordinates
from utils.bresenham import get_bresenham_pixels
from utils.image_reconstruction import add_ray_trace
from utils.filter import filter_sinogram
from utils.sinogram import scan_generate_sinogram
from utils.metrics import calculate_rmse

def interactive_tomograph(img_matrix, N_detectors, distance_between_emitters, angle_coverage, N_scans, use_filter=True):
    print("Trwa prekomputacja pełnego sinogramu. Proszę czekać...")
    
    full_sinogram = scan_generate_sinogram(
        N_detectors, distance_between_emitters, angle_coverage, N_scans, img_matrix
    )
    full_sinogram_np = np.array(full_sinogram)
    actual_scans = len(full_sinogram)
    
    if use_filter:
        print("Trwa nakładanie filtru splotowego na sinogram...")
        active_sinogram = filter_sinogram(full_sinogram)
    else:
        active_sinogram = full_sinogram

    print("Gotowe! Możesz używać suwaka.")

    img_height, img_width = img_matrix.shape
    radius = math.sqrt(pow(img_width, 2) + pow(img_height, 2)) / 2

    output_img_matrix = np.zeros((img_height, img_width))
    ray_counter_matrix = np.zeros((img_height, img_width))
    
    history = {0: (np.copy(output_img_matrix), np.copy(ray_counter_matrix))}

    def update_plot(step):
        nonlocal output_img_matrix, ray_counter_matrix
        
        if step in history:
            output_img_matrix = np.copy(history[step][0])
            ray_counter_matrix = np.copy(history[step][1])
        else:
            last_step = max([k for k in history.keys() if k < step])
            output_img_matrix = np.copy(history[last_step][0])
            ray_counter_matrix = np.copy(history[last_step][1])
            
            for s in range(last_step, step):
                angle = s * (angle_coverage / N_scans)
                
                emiters_cords = calculate_emitter_coordinates(angle, N_detectors, distance_between_emitters, radius, (img_height, img_width))
                detectors_cords = calculate_emitter_coordinates(angle + 180, N_detectors, distance_between_emitters, radius, (img_height, img_width))[::-1]
                
                for i in range(N_detectors):
                    bresenham_pixels = get_bresenham_pixels(emiters_cords[i][0], emiters_cords[i][1], detectors_cords[i][0], detectors_cords[i][1])
                    
                    add_ray_trace(active_sinogram[s][i], bresenham_pixels, output_img_matrix, ray_counter_matrix, (img_height, img_width))
            
            history[step] = (np.copy(output_img_matrix), np.copy(ray_counter_matrix))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        current_sinogram = np.zeros_like(full_sinogram_np)
        current_sinogram[:step] = full_sinogram_np[:step]
        
        ax1.imshow(current_sinogram, cmap='gray', aspect='auto', vmin=full_sinogram_np.min(), vmax=full_sinogram_np.max())
        ax1.set_title(f"Sinogram (skan {step}/{actual_scans-1})")
        ax1.set_xlabel("Indeks detektora")
        ax1.set_ylabel("Kąt (iteracja)")
        
        
        display_img = np.zeros_like(output_img_matrix)
        mask = ray_counter_matrix > 0
        
        if np.any(mask):
            display_img[mask] = output_img_matrix[mask] / ray_counter_matrix[mask]
            
            p_low, p_high = np.percentile(display_img, (30, 98))
            
            if p_low < p_high:
                display_img = exposure.rescale_intensity(display_img, in_range=(p_low, p_high), out_range=(0, 1))

        ax2.imshow(display_img, cmap='gray')
        
        # Obliczanie RMSE jeśli mamy już jakieś dane
        if np.any(mask):
            rmse_val = calculate_rmse(img_matrix, display_img)
            ax2.set_title(f"Rekonstrukcja (RMSE: {rmse_val:.4f})")
        else:
            ax2.set_title("Rekonstrukcja (w toku)")
        
        ax2.axis('off')
        
        plt.tight_layout()
        plt.show()

    slider = widgets.IntSlider(min=0, max=actual_scans-1, step=1, value=0, description='Postęp skanu:', layout=widgets.Layout(width='80%'))
    display(widgets.interact(update_plot, step=slider))