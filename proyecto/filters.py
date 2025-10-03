# Filtros 

__author__ = "Enzo Nicolás Manolucos"

import numpy as np
from scipy.ndimage import uniform_filter, generic_filter

def lee_filter(img, size=3):
    # medias y varianzas locales con filtros uniformes
    mean_local = uniform_filter(img, size)
    mean_sqr_local = uniform_filter(img**2, size)
    var_local = mean_sqr_local - mean_local**2
    
    var_global = np.var(img)
   
    # peso adaptativo
    weights = var_local / (var_local + var_global)
    
    # aplicar filtro
    img_filtered = mean_local + weights * (img - mean_local)

    return img_filtered.astype(np.float32)


def frost_filter(img, size=3, damping=2.0):
    # --- medias y varianzas locales ---
    mean_local = uniform_filter(img, size)
    mean_sqr_local = uniform_filter(img**2, size)
    var_local = mean_sqr_local - mean_local**2
    
    # evitar divisiones por cero
    mean_local = np.where(mean_local == 0, 1e-6, mean_local)
    
    # coeficiente de decaimiento (alpha)
    alpha = damping * (var_local / (mean_local**2))
    
    # kernel de distancias Manhattan
    r = size // 2
    y, x = np.mgrid[-r:r+1, -r:r+1]
    distance = np.abs(x) + np.abs(y)
    
    # salida inicial
    img_filtered = np.zeros_like(img, dtype=np.float32)
    padded = np.pad(img, r, mode='edge')
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+size, j:j+size]
            w = np.exp(-alpha[i, j] * distance)
            w /= np.sum(w)
            img_filtered[i, j] = np.sum(w * window)
    
    return img_filtered.astype(np.float32)


def gamma_map_filter(img, size=5, looks=1):

    def gamma_map_func(window):
        local_mean = np.mean(window)
        local_var  = np.var(window)
        center_val = window[len(window)//2]
        
        numerator   = local_var - (local_mean**2) / looks
        denominator = local_var + local_mean**2
        b = numerator / denominator if denominator != 0 else 0
        b = np.clip(b, 0, 1)
        
        return local_mean * (1 - b) + center_val * b
    
    img_filtered = generic_filter(img, gamma_map_func, size=size, mode='reflect')
    
    return img_filtered.astype(np.float32)
