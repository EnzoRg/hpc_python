import matplotlib.pyplot as plt

def lim(x):
    m = max(x)
    return m + (m * 0.1)

def leer_txt(path):
    d = {}
    with open(path, "r") as f:
        for line in f:
            n, t = line.strip().split(",")
            d[int(n)] = float(t)
    return d

def plot_multiple(files, labels, colors):
    fig = plt.figure()
    fig.set_figheight(6)
    fig.set_figwidth(8)

    tiempo     = plt.subplot2grid(shape=(2, 2), loc=(0, 0), colspan=2, rowspan=1)
    speedup    = plt.subplot2grid(shape=(2, 2), loc=(1, 0), colspan=1, rowspan=1)
    efficiency = plt.subplot2grid(shape=(2, 2), loc=(1, 1), colspan=1, rowspan=1)

    fig.suptitle("Estadísticas de Rendimiento (Comparación)")

    for path, label, color in zip(files, labels, colors):
        times = leer_txt(path)
        x = list(times.keys())
        y = list(times.values())
    
        # SpeedUp:  S = T_s / T_p
        T_s = times[1]    
        S = [T_s / i for i in y]

        # Eficiencia:  E = S / p
        E = [i / j for i, j in zip(S, x)]

        tiempo.plot(x, y, marker="o", color=color, label=label)
        speedup.plot(x, S, marker="d", color=color, label=label)
        efficiency.plot(x, E, marker="s", color=color, label=label)

    tiempo.set_title("Tiempo de ejecución")
    tiempo.set_ylabel("Segundos")
    tiempo.set_xlabel("Número de procesos")
    tiempo.set_xticks(x)
    tiempo.set_ylim(-500, lim(y))
    tiempo.grid(alpha=0.5)
    tiempo.legend()

    speedup.set_title("SpeedUp")
    speedup.set_xlabel("Número de procesos")
    speedup.set_xticks(x)
    speedup.grid(alpha=0.5)
    speedup.legend()

    efficiency.set_title("Eficiencia")
    efficiency.set_xlabel("Número de procesos")
    efficiency.set_xticks(x)
    efficiency.grid(alpha=0.5)
    efficiency.axhline(y=1.0, linewidth=0.6, linestyle="--", color="red")
    efficiency.legend()

    fig.tight_layout(pad=1.5)
    plt.show()
    fig.savefig('proyecto/results/mp_rendimiento.png', dpi=fig.dpi)

archivos = ["proyecto/results/mp_pipeline_10.txt", "proyecto/results/mp_pipeline_100.txt", "proyecto/results/mp_pipeline_1000.txt", "proyecto/results/mp_pipeline_10000.txt"]
labels   = ["Batch 10", "Batch 100", "Batch 1000", "Batch 10000"]
colors   = ["royalblue", "teal", "salmon", "goldenrod"]

plot_multiple(archivos, labels, colors)

