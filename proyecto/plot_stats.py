import matplotlib.pyplot as plt
import sys

def lim(x):
    m = max(x)
    return m + (m * 0.1)

def plot (times, save=True):

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
    tiempo.grid(color='blue', ls = '--', lw = 0.15)
    tiempo.plot(x, y, 'blue', marker='o')

    speedup.set_title("SpeedUp")
    speedup.set_xticks(x)
    speedup.set_ylim(0, lim(S))
    speedup.set_xlabel("Número de procesos")
    speedup.grid(color='green', ls = '--', lw = 0.15)
    # speedup.axhline(y = 1.0, linewidth = 0.5, linestyle = "--", color="green")
    speedup.plot(x, S, 'green', marker='d')

    efficiency.set_title("Eficiencia")
    efficiency.set_xticks(x)
    efficiency.set_ylim(0, lim(E))
    efficiency.set_xlabel("Número de procesos")
    efficiency.grid(color='red', ls = '--', lw = 0.15)
    efficiency.axhline(y = 1.0, linewidth = 0.6, linestyle = "--", color="red")
    efficiency.plot(x, E, 'red', marker='d')

    fig.tight_layout(pad=1.5)

    if save:

        text  = sys.argv[0].replace(".py", ".txt")
        with open(text, 'w') as f:
            for k,v in times.items():
                f.write(str(k) + "," + str(v) + "\n")

        graph = sys.argv[0].replace(".py", ".png")
        plt.savefig(graph, dpi=fig.dpi)

    else:
        plt.show()