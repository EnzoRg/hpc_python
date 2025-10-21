# Introducción a la programación HPC con Python y sus aplicaciones al campo de proceso de imágenes 2025
# Speckle en Imágenes SAR: Evaluación de filtros mediante multiprocesamiento

__author__ = "Enzo Nicolás Manolucos"

# Librerias 
import sys
import pandas as pd
import matplotlib.pyplot as plt

def lim(x):
    m = max(x)
    return m + (m * 0.1)

def hpc_stats(times, name="hpc_stats", save=True):

    fig = plt.figure()
    fig.set_figheight(6)
    fig.set_figwidth(6)

    tiempo     = plt.subplot2grid(shape=(2, 2), loc=(0, 0), colspan=2, rowspan=1)
    speedup    = plt.subplot2grid(shape=(2, 2), loc=(1, 0), colspan=1, rowspan=1)
    efficiency = plt.subplot2grid(shape=(2, 2), loc=(1, 1), colspan=1, rowspan=1)

    x = list(times.keys())
    y = list(times.values())

    # SpeedUp:  S = T_s / T_p
    T_s = times[1]
    S = [T_s / i for i in y]

    # Efficiency:  E = S / p
    E = [i / j for i, j in zip(S, x)]


    fig.suptitle("Estadísticas de Rendimiento")

    tiempo.set_title("Tiempo de ejecución")
    tiempo.set_ylabel("Segundos")
    tiempo.set_xlabel("Número de procesos")
    tiempo.set_xticks(x)
    tiempo.set_ylim(0, lim(y))
    tiempo.grid(alpha=0.5)
    tiempo.plot(x, y, 'royalblue', marker='o')

    speedup.set_title("SpeedUp")
    speedup.set_xticks(x)
    speedup.set_ylim(0, lim(S))
    speedup.set_xlabel("Número de procesos")
    speedup.grid(alpha=0.5)
    speedup.plot(x, S, 'teal', marker='d')

    efficiency.set_title("Eficiencia")
    efficiency.set_xticks(x)
    efficiency.set_ylim(0, lim(E))
    efficiency.set_xlabel("Número de procesos")
    efficiency.grid(alpha=0.5)
    efficiency.axhline(y = 1.0, linewidth = 0.6, linestyle = "--", color="red")
    efficiency.plot(x, E, 'salmon', marker='d')

    fig.tight_layout(pad=1.5)

    if save:

        text  = sys.argv[0].replace(".py", ".txt")
        with open(text, 'w') as f:
            for k,v in times.items():
                f.write(str(k) + "," + str(v) + "\n")

        #graph = sys.argv[0].replace(".py", ".png")
        fig.savefig(f"proyecto/results/{name}.png", dpi=fig.dpi)
        plt.show()

    else:
        plt.show()

    plt.close()

def img_stats(path, name="img_stats", save=True):

    df = pd.read_csv(path)
    #df = df.drop_duplicates()

    # Boxplots
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    df.boxplot(column="psnr", by="filter", ax=ax[0])
    ax[0].set_title("Distribución PSNR por filtro")
    ax[0].set_ylabel("PSNR (dB)")

    df.boxplot(column="ssim", by="filter", ax=ax[1])
    ax[1].set_title("Distribución SSIM por filtro")
    ax[1].set_ylabel("SSIM")

    plt.suptitle("")  
    plt.tight_layout(pad=1.5)

    if save:
        fig.savefig(f"proyecto/results/{name}.png", dpi=fig.dpi)
        plt.show()
    else:
        plt.show()

    plt.close()