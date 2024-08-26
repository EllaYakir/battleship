import numpy as np
import random

class Board:
    def __init__(self, shape=(5, 5)):

        self.layer0 = np.ndarray(shape=shape, dtype=float)
        self.layer0 = self.allocate_pieces(self.layer0, vessels=["Submarine", "General"])

        self.layer1 = np.ndarray(shape=shape, dtype=float)
        self.layer1 = self.allocate_pieces(self.layer1, vessels=["Destroyer", "General"])

        self.layer2 = np.ndarray(shape=shape, dtype=float)
        self.layer2 = self.allocate_pieces(self.layer2, vessels=["Jet", "General"])


    def allocate_pieces(self, layer, number_of_pieces, vessel):
        layer[:] = np.nan
        pieces = [vessel.shape] * number_of_pieces
        for piece in pieces:
            piece_dims = piece.shape.shape
            if len(piece_dims) == 1:
                piece_dims = (piece_dims[0], 1)

            for i in range(50):
                orientation = np.random.randint(0, 2)
                if orientation == 1:
                    height = piece_dims[1]
                    width = piece_dims[0]
                    try:
                        piece.shape = np.rot90(piece.shape, k=-1)
                    finally:
                        piece.shape = piece.shape
                else:
                    height = piece_dims[0]
                    width = piece_dims[1]
                available_slots = self.empty_places(layer, (height, width))
                picked_slot = random.choice(available_slots)


    def empty_places(self, layer, piece_dimensions):
        width = piece_dimensions[0]
        height = piece_dimensions[1]
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
        super().__init__(name="Submarine", shape=np.array([1, 1, 1], dtype=float), layer=0,
                         number_of_pieces=2)
        self.number_of_pieces = 2

    @property
    def is_destroyed(self):
        return bool(np.sum(self.shape) % 1 == 0.5)


class Destroyer(Vessel):
    def __init__(self):
        super().__init__(name="Destroyer", shape=np.array([1, 1, 1, 1], dtype=float), layer=1,
                         number_of_pieces=2)
        self.number_of_pieces = 2

    @property
    def is_destroyed(self):
        return bool(np.all((self.shape - np.floor(self.shape)) == 0.5))


class Jet(Vessel):
    def __init__(self):
        super().__init__(name="Jet", shape=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]], dtype=float), layer=2,
                         number_of_pieces=2)
        self.number_of_pieces = 2

    @property
    def is_destroyed(self):
        return bool(np.sum(self.shape) % 1 == 0.5)


class General(Vessel):
    def __init__(self):
        super().__init__(name="General", shape=np.array([1], dtype=float), layer=np.random.randint(0, 3),
                         number_of_pieces=1)

    @property
    def is_destroyed(self):
        return bool(np.sum(self.shape) % 1 == 0.5)


a = Submarine()
layer = np.ndarray(shape=(5, 5), dtype=float)
layer[:] = np.nan
piece_shape = np.array([1, 1, 1], dtype=float)
#a = empty_places(layer, piece_shape)
n = 1
