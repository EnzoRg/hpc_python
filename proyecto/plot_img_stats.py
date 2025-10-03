# Introducción a la programación HPC con Python y sus aplicaciones al campo de proceso de imágenes 2025
# Speckle en Imágenes SAR: Evaluación de filtros mediante multiprocesamiento

__author__ = "Enzo Nicolás Manolucos"

# Librerias 
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el CSV
df = pd.read_csv("proyecto/img_sar/metricas.csv")

# Promedios
mean_vals = df.groupby("filter")[["psnr", "ssim"]].mean()

# Barras
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

mean_vals["psnr"].plot(kind="bar", ax=ax[0], color=["skyblue", "orange", "green"])
ax[0].set_title("PSNR promedio por filtro")
ax[0].set_ylabel("PSNR (dB)")
ax[0].grid(axis="y", linestyle="--", alpha=0.7)

mean_vals["ssim"].plot(kind="bar", ax=ax[1], color=["skyblue", "orange", "green"])
ax[1].set_title("SSIM promedio por filtro")
ax[1].set_ylabel("SSIM")
ax[1].grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()
fig.savefig('proyecto/results/barras.png', dpi=fig.dpi)

# Boxplots
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

df.boxplot(column="psnr", by="filter", ax=ax[0])
ax[0].set_title("Distribución PSNR por filtro")
ax[0].set_ylabel("PSNR (dB)")

df.boxplot(column="ssim", by="filter", ax=ax[1])
ax[1].set_title("Distribución SSIM por filtro")
ax[1].set_ylabel("SSIM")

plt.suptitle("")  
plt.tight_layout()
fig.savefig('proyecto/results/boxplot.png', dpi=fig.dpi)
plt.show()
