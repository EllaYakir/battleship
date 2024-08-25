class Board:
    def __init__(self):
        self.layer0 = ...
        self. layer1 = ...
        self. layer2 = ...
    pass


class Submarine:
    pass


class Destroyer:
    pass


class Jet:
    pass
#%%
import numpy as np
from matplotlib import pyplot as plt

random_image = np.random.random([500, 500])

plt.imshow(random_image, cmap='gray')
plt.colorbar()