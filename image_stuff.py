from matplotlib import pyplot as plt
import numpy as np


#%%
b = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]])
c = np.rot90(b, 3)
f = 1