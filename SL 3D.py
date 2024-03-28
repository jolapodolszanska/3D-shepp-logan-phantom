import numpy as np
import matplotlib.pyplot as plt

image_size = 256
s_values = np.linspace(-1, 1, image_size)
t_values = np.linspace(-1, 1, image_size)


ellipsoid_params = [
    (0.000, 0.000, 0.000, 0.6900, 0.9200, 0.9000, 0.0, 2.0), # I
    (0.000, 0.000, 0.000, 0.6624, 0.8740, 0.8800, 0.0, -0.98), # II
    (-0.220, 0.000, -0.250, 0.4100, 0.1600, 0.2100, 108.0, -0.02), # III
    (0.220, 0.000, -0.250, 0.3100, 0.1100, 0.2200, 72.0, -0.02), # IV
    (0.000, 0.350, -0.250, 0.2100, 0.2500, 0.5000, 0.0, 0.02), # V 
    (0.000, 0.100, -0.250, 0.0460, 0.0460, 0.0460, 0.0, 0.02), # VI
    (-0.080, -0.650, -0.250, 0.0460, 0.0230, 0.0200, 0.0, 0.01), #VII
    (0.060, -0.650, -0.250, 0.0230, 0.0460, 0.0200, 90.0, 0.01), # VIII
    (0.060, -0.105, 0.625, 0.0400, 0.0560, 0.1000, 90.0, 0.02), # IX
    (0.000, 0.100, 0.625, 0.0560, 0.0400, 0.1000, 0.0, -0.02) # X
]

def calculate_projection_xy(x0, y0, z0, a, b, c, omega, mu, x, y, index):
    omega_radians = np.radians(omega)
    
    # Obrót punktu (x, y) wzgledem srodka ukladu wspolrzednych
    x_rot = y
    y_rot = -x
    
    # Obrót punktu (x_rot, y_rot) do układu współrzędnych elipsy
    if index in [3, 4]:
        omega_radians = -omega_radians
    if index in [8, 9]:
        omega += 90
    if index in [8, 9, 10]:
        omega_radians -= np.pi / 2
        
    x_dim = (x_rot - x0) * np.cos(omega_radians) - (y_rot - y0) * np.sin(omega_radians) + x0
    y_dim = (x_rot - x0) * np.sin(omega_radians) + (y_rot - y0) * np.cos(omega_radians) + y0
    
    # Sprawdzenie, czy punkt znajduje się wewnątrz elipsy
    value = ((x_dim - x0)**2 / a**2) + ((y_dim - y0)**2 / b**2)
    
    # Zwrócenie wartości mu jeśli punkt znajduje się wewnątrz elipsy
    return mu if value <= 1 else 0

def calculate_projection(plane, ellipsoid_params, s_values, t_values):
    projection_grid = np.zeros((image_size, image_size))
    for i, s in enumerate(s_values):
        for j, t in enumerate(t_values):
            for index, (x0, y0, z0, a, b, c, omega, mu) in enumerate(ellipsoid_params, start=1):
                if plane == 'xy' and index not in [9, 10]:  # Pomijamy elipsy 9 i 10 dla projekcji XY
                    mu_value = calculate_projection_xy(x0, y0, z0, a, b, c, omega, mu, s, t, index)
                    projection_grid[i, j] += mu_value
    return projection_grid


def apply_windowing(image, level, width):
    lower_bound = level - width / 2
    upper_bound = level + width / 2
    windowed_image = np.clip(image, lower_bound, upper_bound)
    normalized_image = ((windowed_image - lower_bound) / (upper_bound - lower_bound) * 255).astype(np.uint8)
    return normalized_image

level = 1.02  # center window
width = 0.25  # width window

projections = [calculate_projection(plane, ellipsoid_params, s_values, t_values) for plane in ['xy', 'yz', 'xz']]

adjusted_projection_xy = apply_windowing(projections[0], level, width)

plt.imshow(adjusted_projection_xy, cmap='gray')
plt.show()