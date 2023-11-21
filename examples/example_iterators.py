import numpy as np
import matplotlib.pyplot as plt
from fibrosisoptimization.iterators import (
    BisectionIterator,
    FalsePositionIterator,
    HybridIterator
)


def objective(x, x0=0, y0=-0.25, a=1):
    return y0 + a * (x - x0)**2

# def objective(x):
#     return x**6 - 0.001


def run(iterator):
    iterator.update(0, objective(0))

    x_list = [0]

    for i in range(10):
        x = iterator.next()
        x_list.append(x)
        iterator.update(x, objective(x))

    return np.array(x_list)


x_range = np.linspace(0, 0.6, 100)

bisection = BisectionIterator()
false_postion = FalsePositionIterator()
false_postion.update(0.6, objective(0.6))

hybrid = HybridIterator()

x_bisection = run(bisection)
x_false_position = run(false_postion)
x_false_position = np.insert(x_false_position, 1, 0.6)
x_hybrid = run(hybrid)

fig, axs = plt.subplots(ncols=2)
axs[0].plot(x_range, objective(x_range), label='Target function')
axs[0].scatter(x_hybrid[-1:], objective(x_hybrid[-1:]), c='red',
               label='Solution')
axs[0].grid(True)
axs[0].set_xlabel('x')
axs[0].set_ylabel(r'$f(x)$')
axs[0].legend()

axs[1].grid(True)
axs[1].plot(x_bisection, label='Bisection')
axs[1].plot(x_false_position, label='False-Position')
axs[1].plot(x_hybrid, label='Hybrid')
axs[1].legend()
axs[1].set_xlabel('Iters')
axs[1].set_ylabel('x')

plt.tight_layout()
plt.show()
