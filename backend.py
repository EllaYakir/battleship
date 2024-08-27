import numpy as np
import random
from math import pi
import matplotlib.pyplot as plt

class Board:
    """
    Represents the game board in the 3D Battleship game. Each board has a shape (rows, columns, layers)
    and contains vessels placed in different layers.

    Attributes:
        shape (tuple): Dimensions of the board (rows, columns, layers).
        vessels (dict): A dictionary containing the types of vessels and their respective attributes.
        game_board (np.ndarray): A 3D NumPy array representing the board, where NaN indicates an empty cell.
        vessel_instances (list): A list containing instances of the vessels on the board.
    """

    def __init__(self, shape=(5, 5, 3), vessels={'Submarine': [2, [0]], 'Destroyer': [2, [1]], 'Jet': [1, [2]]}):
        """
        Initializes the game board and allocates vessels to their respective layers.

        Args:
            shape (tuple): The dimensions of the board (rows, columns, layers).
            vessels (dict): A dictionary specifying the types of vessels and their layer assignments.
        """
        self.vessels = vessels
        self.vessels['General'] = [1, [random.randint(0, 2)]]
        self.shape = shape
        self.game_board = np.full(shape, np.nan)  # Use NaN to represent empty cells
        self.vessel_instances = []

        vessel_id_counter = 1
        for layer_number in range(self.shape[2]):
            vessel_id_counter = self.allocate_pieces(layer_number, vessels, vessel_id_counter)

    def allocate_pieces(self, layer_number, vessels, vessel_id_counter):
        """
        Allocates vessels to a specific layer on the board.

        Args:
            layer_number (int): The index of the layer where vessels are to be allocated.
            vessels (dict): The vessels to be placed on the board.
            vessel_id_counter (int): A counter for assigning unique IDs to vessels.

        Returns:
            int: The updated vessel ID counter.
        """
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

            pieces = [vessel_instance.shape] * self.vessels[vessel_name][0]
            color_difference = 0.3

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
                                vessel_instance.vessel_id += color_difference
                                color_difference = color_difference / 2
                                self.vessel_instances.append({vessel_instance: [{'indices': ([row_idx,row_idx + height, layer_number], [column_idx, column_idx + width, layer_number])}, {'hits': 0}]})
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
        """
        Finds all empty places in a specific layer where a vessel piece can fit.

        Args:
            layer (np.ndarray): The 2D array representing a specific layer of the board.
            piece_dimensions (tuple): The dimensions of the piece to be placed.

        Returns:
            list: A list of tuples representing the indices of available slots.
        """
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
    """
    Represents a generic vessel in the game. This is a base class to be inherited by specific vessel types.

    Attributes:
        name (str): The name of the vessel.
        shape (np.ndarray): The shape of the vessel as a 2D or 3D array.
        layer (list): The layers on which the vessel can be placed.
        number_of_pieces (int): The number of pieces this vessel has on the board.
        vessel_id (float): A unique identifier for the vessel.
        hits (np.ndarray): An array tracking the hits received by the vessel.
    """

    def __init__(self, name, shape, layer, number_of_pieces, vessel_id):
        """
        Initializes a generic vessel with the provided attributes.

        Args:
            name (str): The name of the vessel.
            shape (np.ndarray): The shape of the vessel.
            layer (list): The layer(s) where the vessel is placed.
            number_of_pieces (int): The number of pieces of this vessel type on the board.
            vessel_id (float): The unique identifier for the vessel.
        """
        self.name = name
        self.shape = shape
        self.layer = layer
        self.number_of_pieces = number_of_pieces
        self.vessel_id = vessel_id  # Unique identifier for the vessel
        self.hits = np.zeros_like(shape)  # Track hits on this vessel


class Submarine(Vessel):
    """
    Represents a Submarine vessel.

    Attributes:
        shape (np.ndarray): The shape of the Submarine vessel.
    """

    def __init__(self, vessel_id):
        """
        Initializes a Submarine vessel with a unique vessel ID.

        Args:
            vessel_id (float): The unique identifier for the Submarine.
        """
        shape = np.array([1, 1, 1], dtype=float)
        super().__init__(name="Submarine", shape=shape, layer=[0], number_of_pieces=2, vessel_id=vessel_id)

    @property
    def is_destroyed(self):
        """
        Checks if the Submarine is destroyed.

        Returns:
            bool: True if the Submarine is destroyed, False otherwise.
        """
        return np.all(self.hits == 1)  # Destroyed if all parts are hit


class Destroyer(Vessel):
    """
    Represents a Destroyer vessel.

    Attributes:
        shape (np.ndarray): The shape of the Destroyer vessel.
    """

    def __init__(self, vessel_id):
        """
        Initializes a Destroyer vessel with a unique vessel ID.

        Args:
            vessel_id (float): The unique identifier for the Destroyer.
        """
        shape = np.array([1, 1, 1, 1], dtype=float)
        super().__init__(name="Destroyer", shape=shape, layer=[1], number_of_pieces=2, vessel_id=vessel_id)

    @property
    def is_destroyed(self):
        """
        Checks if the Destroyer is destroyed.

        Returns:
            bool: True if the Destroyer is destroyed, False otherwise.
        """
        return np.all(self.hits == 1)  # Destroyed if all parts are hit


class Jet(Vessel):
    """
    Represents a Jet vessel.

    Attributes:
        shape (np.ndarray): The shape of the Jet vessel.
    """

    def __init__(self, vessel_id):
        """
        Initializes a Jet vessel with a unique vessel ID.

        Args:
            vessel_id (float): The unique identifier for the Jet.
        """
        shape = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0], [0, 1, 0]], dtype=float)
        super().__init__(name="Jet", shape=shape, layer=[2], number_of_pieces=2, vessel_id=vessel_id)

    @property
    def is_destroyed(self):
        """
        Checks if the Jet is destroyed.

        Returns:
            bool: True if the Jet is destroyed, False otherwise.
        """
        return np.all(self.hits == 1)  # Destroyed if all parts are hit


class General(Vessel):
    """
    Represents the General vessel. Only one General vessel exists in the game.

    Attributes:
        shape (np.ndarray): The shape of the General vessel.
    """

    def __init__(self, vessel_id):
        """
        Initializes the General vessel with a unique vessel ID.

        Args:
            vessel_id (float): The unique identifier for the General.
        """
        shape = np.array([1], dtype=float)
        super().__init__(name="General", shape=shape, layer=[np.random.randint(0, 2)], number_of_pieces=1, vessel_id=pi)

    @property
    def is_destroyed(self):
        """
        Checks if the General is destroyed.

        Returns:
            bool: True if the General is destroyed, False otherwise.
        """
        return np.all(self.hits == 1)  # Destroyed if all parts are hit


class Game:
    """
    Manages the flow of the game, including player turns, firing, and win condition checks.

    Attributes:
        player1_board (Board): The game board for Player 1.
        player2_board (Board): The game board for Player 2.
        current_turn (int): Tracks whose turn it is (1 or 2).
    """

    def __init__(self):
        """
        Initializes the game, sets up the board, and assigns the current turn.
        """
        board_size, vessels = setup_game()
        self.player1_board = Board(shape=board_size, vessels=vessels)
        self.player2_board = Board(shape=board_size, vessels=vessels)
        self.current_turn = 1

    def get_player_input(self):
        """
        Gets input from the current player for the target coordinates.

        Returns:
            tuple: A tuple containing the row, column, and layer of the targeted cell.
        """
        while True:

            try:
                to_see_or_not_to_see = input("To see your board, enter \"show\". To continue, press Enter.\n")
                if to_see_or_not_to_see.lower() == "show":
                    current_board = self.player1_board if self.current_turn == 1 else self.player2_board
                    self.show_board(current_board)
                layer = int(input("Enter layer (0-2): "))
                row = int(input("Enter row: "))
                col = int(input("Enter column: "))

                if not (0 <= row < self.player1_board.shape[0] and
                        0 <= col < self.player1_board.shape[1] and
                        0 <= layer < self.player1_board.shape[2]):
                    print("Invalid coordinates, please enter values within board bounds.")
                    continue
                return row, col, layer
            except ValueError:
                print("Invalid input, please enter integers only.")

    def switch_turn(self):
        """
        Switches the turn from one player to the other.
        """
        self.current_turn = 2 if self.current_turn == 1 else 1

    def get_current_board(self):
        """
        Gets the board of the current player.

        Returns:
            Board: The board of the current player.
        """
        return self.player1_board if self.current_turn == 1 else self.player2_board

    def get_opponent_board(self):
        """
        Gets the board of the opponent player.

        Returns:
            Board: The board of the opponent player.
        """
        return self.player2_board if self.current_turn == 1 else self.player1_board

    def fire_at(self, row, col, layer):
        """
        Fires at a specified coordinate on the opponent's board.

        Args:
            row (int): The row index of the target.
            col (int): The column index of the target.
            layer (int): The layer index of the target.

        Returns:
            tuple: A tuple where the first element is a boolean indicating if a hit was made,
                   and the second element is the vessel that was hit (or None if no hit).
        """
        opponent_board = self.get_opponent_board()
        target_id = opponent_board.game_board[row, col, layer]

        for item in opponent_board.vessel_instances:
            indices = list(list(item.values())[0][0].values())[0]
            if row in np.arange(indices[0][0],indices[0][1]) and col in np.arange(indices[1][0],indices[1][1]):
                opponent_board.vessel_instances.remove(item)
                print("KILL")
            else:
                print("MISS")


    def check_for_win(self, board):
        """
        Checks if the game is over by verifying the win conditions.

        Args:
            board (Board): The board of the player being checked.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        for vessel in board.vessel_instances:
            if vessel.name == "General" and vessel.is_destroyed:
                print("General was hit. Game over!")
                return True
            elif vessel.name != "General" and not vessel.is_destroyed:
                return False
        return True

    def take_turn(self):
        """
        Manages a single turn in the game.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        print(f"Player {self.current_turn}'s turn")
        row, col, layer = self.get_player_input()

        self.fire_at(row, col, layer)
        self.switch_turn()
        return False

    def show_board(self, current_board):
        """
        Displays the current state of the player's board.

        Args:
            current_board (Board): The board of the current player.
        """
        layers = [current_board.game_board[:, :, 0], current_board.game_board[:, :, 1],
                  current_board.game_board[:, :, 2]]
        layer_titles = ["Deep Sea Layer", "Sea-Level Layer", "Air Layer"]  # Titles for each subplot

        plt.figure(figsize=(8, 12))
        for index, layer in enumerate(layers):
            ax = plt.subplot(3, 1, index + 1)  # Create subplot first

            # Plot the layer using the colormap
            plt.pcolormesh(layer, cmap='viridis', edgecolors='k', linewidth=2)
            ax.set_aspect('equal')
            ax.invert_yaxis()
            ax.set_xticks(np.arange(0, layer.shape[1]))  # Fixed the range for xticks and yticks
            ax.set_yticks(np.arange(0, layer.shape[0]))
            ax.tick_params(top=True, labeltop=True)
            ax.set_title(layer_titles[index])  # Set the title for each subplot

        plt.tight_layout()  # Adjusts the layout so titles and labels fit without overlapping
        plt.show()  # Show all subplots together after the loop

    def play(self):
        """
        Starts the game and manages the game loop until the game is over.
        """
        game_over = False
        while not game_over:
            game_over = self.take_turn()
        print("Game over!")


def setup_game():
    """
    Sets up the game by asking the user for board dimensions and the number of vessels.

    Returns:
        tuple: A tuple containing the board dimensions and the vessel configuration.
    """
    print("Welcome to the 3D Battleship Game!")

    # Get board dimensions
    while True:
        try:
            rows = int(input("Enter the number of rows for the board: "))
            cols = int(input("Enter the number of columns for the board: "))
            layers = 3  # Always 3 layers as per the game rules
            if rows > 0 and cols > 0:
                break
            else:
                print("Rows and columns must be positive integers.")
        except ValueError:
            print("Please enter valid integers.")

    # Get the number of vessels
    vessels = {}
    for vessel_name in ["Submarine", "Destroyer", "Jet"]:
        while True:
            try:
                num_vessels = int(input(f"Enter the number of {vessel_name}s: "))
                if num_vessels >= 0:
                    if vessel_name == "Submarine":
                        vessels["Submarine"] = [num_vessels, [0]]
                    elif vessel_name == "Destroyer":
                        vessels["Destroyer"] = [num_vessels, [1]]
                    elif vessel_name == "Jet":
                        vessels["Jet"] = [num_vessels, [2]]
                    break
                else:
                    print("Number of vessels must be a non-negative integer.")
            except ValueError:
                print("Please enter a valid integer.")

    vessels["General"] = [1, [random.randint(0, 2)]]  # Only one General allowed

    return (rows, cols, layers), vessels


if __name__ == "__main__":
    game = Game()
    game.play()
