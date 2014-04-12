import matplotlib.pyplot as plt
import numpy as np
import scipy
import random as r

x = np.linspace(0, 1.0, num = 9)
y = np.array([r.uniform(-1, 1) for _ in xrange(8)])
y = np.append(y, y[0])
impulse = np.polyfit(x, y, 10)
p = np.poly1d(impulse)
