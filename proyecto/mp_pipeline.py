# Introducción a la programación HPC con Python y sus aplicaciones al campo de proceso de imágenes 2025
# Speckle en Imágenes SAR: Evaluación de filtros mediante multiprocesamiento

__author__ = "Enzo Nicolás Manolucos"

# Librerias 
import os 
import cv2
import csv
import time
import numpy as np
import multiprocessing as mp

from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

from filters import lee_filter, frost_filter, gamma_map_filter
from plot_stats import hpc_stats, img_stats

# Rutas -> Eliminar test
base_path = "proyecto/data_sar_test"
csv_path = "proyecto/data_sar_test/metricas.csv"
results_path = "proyecto/results_test"

def guardar_csv(resultados):

    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image", "filter", "psnr", "ssim"])
        for grupo in resultados:
            writer.writerows(grupo)


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

def procesar_imagen(imagen, show_metrics=False):

    # Nombre de las carpetas acorde a los filtros utilizados
    resultados = []
    filtros = ["lee", "frost", "gamma"]

    for filtro in filtros:

        # Carpetas 
        os.makedirs(f"{base_path}/{filtro}", exist_ok = True)
        noise_path  = f"{base_path}/noise/{imagen}"
        clean_path = f"{base_path}/clean/{imagen}"
        result_path = f"{base_path}/{filtro}/{imagen}"

        # Leer imágen con speckle (noise) y limpia 
        img_noise = cv2.imread(noise_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)
        img_clean = cv2.imread(clean_path, cv2.IMREAD_GRAYSCALE)

        # Filtrar imágen 
        img_filt = filtrar_imagen(img_noise, filtro)

        # Calcular métricas
        img_psnr = psnr(img_clean, img_filt, data_range=255)
        img_ssim = ssim(img_clean, img_filt, data_range=255)  
        resultados.append((imagen, filtro, img_psnr, img_ssim))

        if show_metrics:
            print(f"Filtro: {filtro}\tImagen: {imagen}\tPSNR: {img_psnr:.4f}\tSSIM: {img_ssim:.4f}")

        # Guardar imagen en formato uint8
        img_norm = cv2.normalize(img_filt, None, 0, 255, cv2.NORM_MINMAX)
        img_uint8 = img_norm.astype(np.uint8)
        cv2.imwrite(result_path, img_uint8)

    return resultados

def main(base_path):

    # Datos
    image_names = list()
    times = dict()

    # Carpetas 
    folder_in = os.path.join(base_path, "noise")

    for image in os.listdir(folder_in):
        if (image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg")):
            image_names.append(image) 
    
    # Número de procesadores
    num_proc = mp.cpu_count()

    for p in range(1, num_proc + 1):

        print(f"Número de procesos: {p}")

        start = time.time()

        with mp.Pool(processes=p) as pool:
            resultados = pool.map(procesar_imagen, image_names)

        end = time.time()

        duration = end - start

        print(f"Tiempo: {duration:.4f} s\n")

        times[p] = duration

        if p == num_proc:
            guardar_csv(resultados)

    hpc_stats(times, "mp_hpc_stats", True)
    img_stats(csv_path, "mp_img_stats", True)

if __name__ == '__main__':
    main(base_path)
