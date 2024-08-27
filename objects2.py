import numpy as np
import random
from math import pi


class Board:
    def __init__(self, shape=(5, 5, 3), vessels={'Submarine': [2, [0]], 'Destroyer': [2, [1]], 'Jet': [1, [2]]}):

        self.vessels = vessels
        self.vessels['General'] = [1, [random.randint(0, 2)]]

        self.shape = shape
        self.game_board = np.ndarray(shape=shape, dtype=float)

        for layer_number in range(self.shape[2]):
            self.game_board[:, :, layer_number] = self.allocate_pieces(layer_number, vessels)


    def allocate_pieces(self, layer_number, vessels):
        layer = np.ndarray(shape=self.shape[0:2], dtype=float)
        layer[:] = np.nan
        this_layer_vessels = [key for key, value in vessels.items() if layer_number in value[1]]
        this_layer_vessels_dict = {}
        for ind, vessel in enumerate(this_layer_vessels):
            """Add more conditions if other types of vessels are added"""
            if vessel == 'Submarine':
                this_layer_vessels_dict['Submarine'] = Submarine()
            if vessel == 'Destroyer':
                this_layer_vessels_dict['Destroyer'] = Destroyer()
            if vessel == 'Jet':
                this_layer_vessels_dict['Jet'] = Jet()
            if vessel == 'General':
                this_layer_vessels_dict['General'] = General()

        for key, value in this_layer_vessels_dict.items():
            if key == 'General':
                pieces = [value.shape * pi]
            else:
                pieces = [value.shape] * self.vessels[key][0]

            for piece, n in enumerate(pieces, 1):
                piece = piece * n
                piece_dims = piece.shape
                if len(piece_dims) == 1:
                    piece_dims = (1, piece_dims[0])
                    piece = piece.reshape(piece_dims)

                for i in range(50):
                    orientation = np.random.randint(0, 2)
                    if orientation == 1:
                        height = piece_dims[1]
                        width = piece_dims[0]
                        piece = np.rot90(piece, k=-1)
                    else:
                        height = piece_dims[0]
                        width = piece_dims[1]
                    available_slots = self.empty_places(layer, (height, width))
                    if len(available_slots) != 0:
                        picked_slot = random.choice(available_slots)
                        row_idx = picked_slot[0]
                        column_idx = picked_slot[1]
                        if row_idx+height > layer.shape[0] or column_idx+width > layer.shape[1]:
                            continue
                        else:
                            layer[row_idx:row_idx+height, column_idx:column_idx+width] = piece
                            break
                    else:
                        if i == 49:
                            raise Exception("Board initialization failed. Try again with less vessels or with a larger"
                                            " board.")
                        else:
                            continue
        layer[layer == 0] = np.nan
        return layer

    def empty_places(self, layer, piece_dimensions):
        height = piece_dimensions[0]
        width = piece_dimensions[1]
        seed_idx = []
        for index, cell_content in np.ndenumerate(layer):
            row_idx = index[0]
            column_idx = index[1]
            if row_idx + height <= layer.shape[0] and column_idx + width <= layer.shape[1]:
                this_slice = layer[row_idx:row_idx + height, column_idx:column_idx + width]
                if np.isnan(this_slice).all():
                    seed_idx.append(index)
        return seed_idx


class Vessel:
    def __init__(self, name, shape, layer, number_of_pieces):
        self.name = name
        self.shape = shape
        self.layer = layer
        self.number_of_pieces = number_of_pieces


class Submarine(Vessel):
    def __init__(self):
        super().__init__(name="Submarine", shape=np.array([1, 1, 1], dtype=float), layer=[0],
                         number_of_pieces=2)
        self.number_of_pieces = 2

    @property
    def is_destroyed(self):
        return bool(np.sum(self.shape) % 1 == 0.5)


class Destroyer(Vessel):
    def __init__(self):
        super().__init__(name="Destroyer", shape=np.array([1, 1, 1, 1], dtype=float), layer=[1],
                         number_of_pieces=2)
        self.number_of_pieces = 2

    @property
    def is_destroyed(self):
        return bool(np.all((self.shape - np.floor(self.shape)) == 0.5))


class Jet(Vessel):
    def __init__(self):
        super().__init__(name="Jet", shape=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]], dtype=float),
                         layer=[2], number_of_pieces=2)
        self.number_of_pieces = 2

    @property
    def is_destroyed(self):
        return bool(np.sum(self.shape) % 1 == 0.5)


class General(Vessel):
    def __init__(self):
        super().__init__(name="General", shape=np.array([1], dtype=float), layer=[np.random.randint(0, 2)],
                         number_of_pieces=1)

    @property
    def is_destroyed(self):
        return bool(np.sum(self.shape) % 1 == 0.5)
