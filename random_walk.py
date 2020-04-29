import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def randPosInit(x_min, x_max, y_min, y_max):
    x = np.random.randint(x_min, x_max)
    y = np.random.randint(y_min, y_max)

    return x, y


# 0 = infected, 1 = healthy, 2 = imune
def procIsInfect():
    rd = np.random.uniform(0, 1) * 100
    if rd < ratio_infec:
        return 0
    return 1


def update(individu, individus):
    x, y, infection_time, healthy = individu

    _prob_moving = np.random.uniform(0, 1)

    if _prob_moving < (prob_moving / 100):
        d = np.random.uniform(0, 1)

        if d <= .25:
            x = x + 1
        elif d <= .50:
            y = y - 1
        elif d <= .75:
            x = x - 1
        else:
            y = y + 1

    if healthy is 0:
        infection_time = infection_time + 1

    if infection_time > day_to_recover:
        healthy = 2

    if any(elem is not individu and elem[0] == individu[0] and elem[1] == individu[1] for elem in individus) and healthy is not 2:
        healthy = 0

    return x, y, infection_time, healthy


def isFinite(x, y, x_min, x_max, y_min, y_max, x_range, y_range):
    if x > x_max:
        x = x - x_range
    if x < x_min:
        x = x + x_range

    if y > y_max:
        y = y - y_range

    if y < y_min:
        y = y + y_range

    return x, y


def animate(i):
    # [[30,30,31], [31,31,23]]
    # do refactor shape ?? reshape
    x_anim.append([])
    y_anim.append([])
    for j in range(n_individu):
        x_anim[i].append([])
        y_anim[i].append([])

        individu = history[i][j]

        x_anim[i][j] = individu[0]
        y_anim[i][j] = individu[1]

    for j, c in enumerate(individus):
        individu = history[i][j]

        c.set_color(colors[individu[3]])
        c.set_data(x_anim[i][j], y_anim[i][j])

    return individus


def init():
    for individu in individus:
        individu.set_data([], [])

    return individus


if __name__ == "__main__":

    x_max = 20
    x_min = 0
    y_max = 20
    y_min = 0

    x_range = x_max - x_min
    y_range = y_max - y_min

    n_individu = 200

    ratio_infec = 5
    prob_moving = 80
    day_to_recover = 10

    history = []
    # inisialisasi posisi individu
    history.append([])
    for i in range(0, n_individu):
        x, y = randPosInit(x_min, x_max, y_min, y_max)

        healthy = procIsInfect()
        infection_time = 0

        individu = (x, y, infection_time, healthy)
        history[0].append(individu)

    i = 1
    while True:
        history.append([])
        for j in range(0, n_individu):
            x = history[i-1][j][0]
            y = history[i-1][j][1]

            x, y, infection_time, healthy = update(
                history[i-1][j], history[i-1])

            x, y = isFinite(x, y, x_min, x_max, y_min, y_max, x_range, y_range)

            individu = (x, y, infection_time, healthy)
            history[i].append(individu)

        if all(individu[3] > 0 for individu in history[i]):
            break
        i = i + 1

    df = pd.DataFrame(history[0:])
    print(df)

    x = [i for i in range(len(history))]
    y = [len([tup[3] for tup in hist if tup[3] == 0]) for hist in history]

    plt.figure()
    plt.plot(x, y)

    plt.ylabel("Count of infected")
    plt.xlabel("Count of day")
    plt.title("Count of Infected to Virus each day")
    plt.savefig('infected_line_chart.png')

    fig, _ = plt.subplots()
    axes = plt.axes(xlim=(x_min, x_max), ylim=(x_min, x_max))
    colors = ['red', 'blue', 'green']
    
    axes.legend()

    individus = []
    x_anim = []
    y_anim = []

    # inisialisasi animasi
    for i in range(n_individu):
        individus.append(axes.plot([], [], 'o', markersize=5, lw=1)[0])

    myAnimation = animation.FuncAnimation(fig, func=animate,
                                          repeat=True, init_func=init, frames=len(history))
    myAnimation.save('random_walk_animation.gif',
                     writer='PillowWriter')
