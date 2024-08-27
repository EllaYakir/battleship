import numpy as np
import random


class Board:
    def __init__(self, shape=(5, 5, 3), vessels={'Submarine': [2, [0]], 'Destroyer': [2, [1]], 'Jet': [1, [2]]}):
        self.vessels = vessels
        self.vessels['General'] = [1, [random.randint(0, 2)]]
        self.shape = shape
        self.game_board = np.full(shape, np.nan)  # Use NaN to represent empty cells
        self.vessel_instances = []

        vessel_id_counter = 1
        for layer_number in range(self.shape[2]):
            vessel_id_counter = self.allocate_pieces(layer_number, vessels, vessel_id_counter)

    def allocate_pieces(self, layer_number, vessels, vessel_id_counter):
        layer = self.game_board[:, :, layer_number]
        this_layer_vessels = [key for key, value in vessels.items() if layer_number in value[1]]
        this_layer_vessels_dict = {}

        for vessel_name in this_layer_vessels:
            if vessel_name == 'Submarine':
                vessel_instance = Submarine(vessel_id_counter)
            elif vessel_name == 'Destroyer':
                vessel_instance = Destroyer(vessel_id_counter)
            elif vessel_name == 'Jet':
                vessel_instance = Jet(vessel_id_counter)
            elif vessel_name == 'General':
                vessel_instance = General(vessel_id_counter)

            this_layer_vessels_dict[vessel_name] = vessel_instance
            self.vessel_instances.append(vessel_instance)

            pieces = [vessel_instance.shape] * self.vessels[vessel_name][0]

            for piece in pieces:
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
                    if available_slots:
                        picked_slot = random.choice(available_slots)
                        row_idx = picked_slot[0]
                        column_idx = picked_slot[1]
                        if row_idx + height > layer.shape[0] or column_idx + width > layer.shape[1]:
                            continue
                        else:
                            try:
                                layer[row_idx:row_idx + height, column_idx:column_idx + width] = piece * vessel_instance.vessel_id
                                break
                            except:
                                if i == 49:
                                    raise Exception("Board initialization failed. Try again with fewer vessels or with"
                                                    " a larger board.")
                                else:
                                    continue

                    else:
                        if i == 49:
                            raise Exception(
                                "Board initialization failed. Try again with fewer vessels or with a larger board.")
            vessel_id_counter += 1
        layer[layer == 0] = np.nan
        self.game_board[:, :, layer_number] = layer
        return vessel_id_counter

    def empty_places(self, layer, piece_dimensions):
        height = piece_dimensions[0]
        width = piece_dimensions[1]
        seed_idx = []
        for index, cell_content in np.ndenumerate(layer):
            row_idx = index[0]
            column_idx = index[1]
            if row_idx + height <= layer.shape[0] and column_idx + width <= layer.shape[1]:
                this_slice = layer[row_idx:row_idx + height, column_idx:column_idx + width]
                if np.isnan(this_slice).all():  # Ensure the slot is completely empty
                    seed_idx.append(index)
        return seed_idx


class Vessel:
    def __init__(self, name, shape, layer, number_of_pieces, vessel_id):
        self.name = name
        self.shape = shape
        self.layer = layer
        self.number_of_pieces = number_of_pieces
        self.vessel_id = vessel_id  # Unique identifier for the vessel
        self.hits = np.zeros_like(shape)  # Track hits on this vessel

class Submarine(Vessel):
    def __init__(self, vessel_id):
        shape = np.array([1, 1, 1], dtype=float)
        super().__init__(name="Submarine", shape=shape, layer=[0], number_of_pieces=2, vessel_id=vessel_id)

    @property
    def is_destroyed(self):
        return np.all(self.hits == 1)  # Destroyed if all parts are hit

class Destroyer(Vessel):
    def __init__(self, vessel_id):
        shape = np.array([1, 1, 1, 1], dtype=float)
        super().__init__(name="Destroyer", shape=shape, layer=[1], number_of_pieces=2, vessel_id=vessel_id)

    @property
    def is_destroyed(self):
        return np.all(self.hits == 1)  # Destroyed if all parts are hit

class Jet(Vessel):
    def __init__(self, vessel_id):
        shape = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]], dtype=float)
        super().__init__(name="Jet", shape=shape, layer=[2], number_of_pieces=2, vessel_id=vessel_id)

    @property
    def is_destroyed(self):
        return np.all(self.hits == 1)  # Destroyed if all parts are hit

class General(Vessel):
    def __init__(self, vessel_id):
        shape = np.array([1], dtype=float)
        super().__init__(name="General", shape=shape, layer=[np.random.randint(0, 2)], number_of_pieces=1, vessel_id=vessel_id)

    @property
    def is_destroyed(self):
        return np.all(self.hits == 1)  # Destroyed if all parts are hit
