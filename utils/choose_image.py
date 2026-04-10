import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

class Choose_image:
    def __init__(self, folder_path='./src/example_images/'):
        self.folder_path = folder_path
        self.img_matrix = None
        self.img_height = 0
        self.img_width = 0
        
        # Pobieranie listy plików
        self.images_list = [
            f for f in os.listdir(folder_path) 
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tif'))
        ]
        
        # Inicjalizacja widgetów
        self.dropdown = widgets.Dropdown(
            options=self.images_list,
            value=self.images_list[0] if self.images_list else None,
            description='Obraz:',
        )
        self.output_area = widgets.Output()
        
        # Podpięcie zdarzenia
        self.dropdown.observe(self._on_change, names='value')

    def _on_change(self, change):
        self.process_image(change['new'])

    def process_image(self, file_name):
            # Deklarujemy, że chcemy modyfikować zmienne na poziomie notebooka
            global img_matrix, img_height, img_width 
            
            with self.output_area:
                clear_output(wait=True)
                file_path = os.path.join(self.folder_path, file_name)
                try:
                    img = Image.open(file_path).convert('L')
                    
                    # Aktualizacja atrybutów instancji (wewnątrz klasy)
                    self.img_matrix = np.array(img) / 255
                    self.img_height, self.img_width = self.img_matrix.shape
                    
                    # Aktualizacja zmiennych globalnych (widocznych w notebooku)
                    img_matrix = self.img_matrix
                    img_height = self.img_height
                    img_width = self.img_width
                    
                    print(f"Plik: {file_name} | Rozmiar: {img_height}x{img_width}")
                    
                    plt.figure(figsize=(6, 6))
                    plt.imshow(img_matrix, cmap='gray')
                    plt.axis('off')
                    plt.show()
                except Exception as e:
                    print(f"Błąd ładowania pliku {file_name}: {e}")

    def show(self):
        """Wyświetla UI i ładuje pierwszy obrazek"""
        display(self.dropdown)
        display(self.output_area)
        if self.dropdown.value:
            self.process_image(self.dropdown.value)