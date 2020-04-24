import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation 


def randInit(x_min, x_max, y_min, y_max):
    x = np.random.randint(x_min, x_max)
    y = np.random.randint(y_min, y_max)

    return x, y

def update(x, y):
    d = np.random.uniform(0, 1)

    if d <= .25:
        x = x + 1
    elif d <= .50:
        y = y - 1
    elif d <= .75:
        x = x - 1
    else:
        y = y + 1
    return x, y

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
    for j in range(n_particle):
        x_anim[j][i] = history[i][j][0]
        y_anim[j][i] = history[i][j][1]
        
    for j, particle in enumerate(particles):
        particle.set_data(x_anim[j], y_anim[j])
    
    return particles

def init():
    for particle in particles:
        particle.set_data([], [])
    
    return particles

if __name__ == "__main__":

    x_max = 100
    x_min = -100
    y_max = 100
    y_min = -100

    x_range = x_max - x_min
    y_range = y_max - y_min

    n_particle = 10
    n_iter = 100

    history = np.empty((n_iter, n_particle), dtype=tuple)

    for i in range(0, n_particle):
        x, y = randInit(x_min, x_max, y_min, y_max)

        particle = (x, y)
        history[0][i] = particle

    for i in range(1, n_iter):
        for j in range(0, n_particle):
            x = history[i-1][j][0]
            y = history[i-1][j][1]

            x, y = update(x, y)

            x, y = isFinite(x, y, x_min, x_max, y_min, y_max, x_range, y_range)
            
            history[i][j] = (x, y)
                
    df = pd.DataFrame(history[0:])
    print(df)

    fig,_ = plt.subplots()
    axes = plt.axes(xlim=(x_min, x_max), ylim=(x_min, x_max))
    colors = ['green', 'black', 'red', 'blue', 'purple', 'yellow', 'grey','orange', 'pink', 'brown']

    particles = []
    x_anim = np.empty((n_particle, n_iter), dtype=tuple)
    y_anim = np.empty((n_particle, n_iter), dtype=tuple)

    for i in range(n_particle):
        particles.append(axes.plot([], [], 'o', markersize=1, lw=1,  color=colors[i])[0])

    
    myAnimation = animation.FuncAnimation(fig, func=animate, \
    repeat=True, init_func=init, frames=n_iter)

    myAnimation.save('random_walk_animation.gif', writer='PillowWriter', fps=30)