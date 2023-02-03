import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

# Test : Plotting recieved damaged based on armor and base damage

def f(x, d):
    # Armor formula from 
    condition = np.where((x > (d / 2)) > 0, 1, 0)
    return (((d*d) / (4 * x)) * condition) + ((1 - condition) * (d - x))

x = np.linspace(5, 150, 50)
d = np.linspace(5, 200, 60)
X, D = np.meshgrid(x, d)
Y = f(X, D)

# Set up plot
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

surf = ax.plot_surface(X, D, Y, cmap=cm.coolwarm, linewidth=0, antialiased=False)
ax.set_xlabel("armor")
ax.set_ylabel("damage")

ax.zaxis.set_major_locator(LinearLocator(10))
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()