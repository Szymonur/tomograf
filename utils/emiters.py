import numpy as np

def calculate_emitter_coordinates(alpha_deg, num_emiters, distance_between, radius, image_shape):
    """
    alpha_deg: aktualny kąt obrotu w stopniach
    num_emiters: liczba emiterów (detektorów)
    distance_between: odległość między sąsiednimi emiterami (w pikselach)
    radius: promień na jakim znajduje się głowica od środka obrazu
    image_shape: krotka (height, width) obrazu wejściowego
    """
    
    # 1. Konwersja kąta na radiany
    alpha = np.radians(alpha_deg)
    
    # 2. Wyznaczenie środka obrazu (punkt odniesienia)
    center_x = image_shape[1] / 2
    center_y = image_shape[0] / 2
    
    # 3. Wyznaczenie centralnego punktu głowicy (środek linii emiterów)
    # Głowica krąży po okręgu o promieniu 'radius'
    head_center_x = center_x + radius * np.cos(alpha)
    head_center_y = center_y + radius * np.sin(alpha)
    
    # 4. Wyznaczenie wektora prostopadłego do kierunku naświetlania
    # To po tej linii będziemy "rozsuwać" emitery
    # Wektor prostopadły do [cos(a), sin(a)] to [-sin(a), cos(a)]
    v_x = -np.sin(alpha)
    v_y = np.cos(alpha)
    
    emiters = []
    
    # 5. Wyznaczenie pozycji każdego emitera
    # Chcemy, aby emitery były rozłożone symetrycznie względem head_center
    offset_start = -((num_emiters - 1) * distance_between) / 2
    
    for i in range(num_emiters):
        current_offset = offset_start + i * distance_between
        
        # Nowe współrzędne = środek głowicy + przesunięcie wzdłuż wektora v
        ex = head_center_x + current_offset * v_x
        ey = head_center_y + current_offset * v_y
        
        emiters.append((ex.item(), ey.item()))
        
    return emiters

