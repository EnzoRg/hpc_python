# Introducción a la programación HPC con Python y sus aplicaciones al campo de proceso de imágenes 2025
# Speckle en Imágenes SAR: Evaluación de filtros mediante multiprocesamiento

__author__ = "Enzo Nicolás Manolucos"

# Librerias 
import os 
import cv2
import csv
import json
import time
import numpy as np
import multiprocessing as mp

from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

from filters import lee_filter, frost_filter, gamma_map_filter
from plot_stats import plot 

# Rutas
base_path = "proyecto/data_sar"
csv_path = "proyecto/data_sar/metricas.csv"
results_path = "proyecto/results"

def guardar_csv(imagen, filtro, psnr_val, ssim_val):

    # Guardar métricas
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:  
            writer.writerow(["image", "filter", "psnr", "ssim"])
        writer.writerow([imagen, filtro, f"{psnr_val:.4f}", f"{ssim_val:.4f}"])


def filtrar_imagen(img, folder):

    # Filtros
    if folder == "lee":
        return lee_filter(img, 3)
    elif folder == "frost":
        return frost_filter(img, 3, 2.0)
    elif folder == "gamma":
        return gamma_map_filter(img, 5, 1)
    else: 
        return img  

def procesar_imagen(imagen):

    # Nombre de las carpetas acorde a los filtros utilizados
    folders = ["lee", "frost", "gamma"]

    for folder in folders:

        # Carpetas 
        os.makedirs(f"{base_path}/{folder}", exist_ok = True)
        noise_path  = f"{base_path}/noise/{imagen}"
        clean_path = f"{base_path}/clean/{imagen}"
        result_path = f"{base_path}/{folder}/{imagen}"

        # Leer imágen con speckle (noise) y limpia 
        img_noise = cv2.imread(noise_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)
        img_clean = cv2.imread(clean_path, cv2.IMREAD_GRAYSCALE)

        # Filtrar imágen 
        img_filt = filtrar_imagen(img_noise, folder)
        metricas(img_filt, img_clean, imagen, folder)

        # Guardar imagen en formato uint8
        img_norm = cv2.normalize(img_filt, None, 0, 255, cv2.NORM_MINMAX)
        img_uint8 = img_norm.astype(np.uint8)
        cv2.imwrite(result_path, img_uint8)


def metricas(img_filt, img_clean, image, filter):

    # Calcular PSNR y SSIM
    img_psnr = psnr(img_clean, img_filt, data_range=255)
    img_ssim = ssim(img_clean, img_filt, data_range=255)  

    print(f"Filtro: {filter}\tImagen: {image}\tPSNR: {img_psnr:.4f}\tSSIM: {img_ssim:.4f}")  
    guardar_csv(image, filter, img_psnr, img_ssim)


def main(base_path):
    
    # Número de procesadores
    num_proc = mp.cpu_count()

    times = dict()

    folder_in = os.path.join(base_path, "noise")

    for p in range(1, num_proc + 1):

        start = time.time()
        image_names = list()

        for image in os.listdir(folder_in):
            if (image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg")):
                image_names.append(image)    

        with mp.Pool(processes=p) as pool:
            pool.map(procesar_imagen, image_names)

        end = time.time()

        print("Num. Procesadores:", p, " Tiempo:", end - start)

        times[p] = end - start

    plot(times)

if __name__ == '__main__':
    main(base_path)