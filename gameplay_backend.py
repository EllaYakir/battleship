from objects import *


class Game:
    def __init__(self):
        board_size, vessels = setup_game()
        self.player1_board = Board(shape=board_size, vessels=vessels)
        self.player2_board = Board(shape=board_size, vessels=vessels)
        self.current_turn = 1

    def get_player_input(self):
        while True:
            try:
                row = int(input("Enter row: "))
                col = int(input("Enter column: "))
                layer = int(input("Enter layer (0-2): "))
                if not (0 <= row < self.player1_board.shape[0] and
                        0 <= col < self.player1_board.shape[1] and
                        0 <= layer < self.player1_board.shape[2]):
                    print("Invalid coordinates, please enter values within board bounds.")
                    continue
                return row, col, layer
            except ValueError:
                print("Invalid input, please enter integers only.")

    def switch_turn(self):
        self.current_turn = 2 if self.current_turn == 1 else 1

    def get_current_board(self):
        return self.player1_board if self.current_turn == 1 else self.player2_board

    def get_opponent_board(self):
        return self.player2_board if self.current_turn == 1 else self.player1_board

    def fire_at(self, row, col, layer):
        opponent_board = self.get_opponent_board()
        target_id = opponent_board.game_board[row, col, layer]

        if not np.isnan(target_id):
            for vessel in opponent_board.vessel_instances:
                if vessel.vessel_id == target_id:
                    vessel.hits += 1  # Mark the hit on the vessel
                    opponent_board.game_board[row, col, layer] = vessel.vessel_id + 0.5  # Mark the cell as hit
                    return True, vessel
        return False, None

    def check_for_win(self, board):
        for vessel in board.vessel_instances:
            if vessel.name == "General" and vessel.is_destroyed:
                print("General has been hit!")
                return True
            elif vessel.name != "General" and not vessel.is_destroyed:
                return False
        return True

    def take_turn(self):
        print(f"Player {self.current_turn}'s turn")
        row, col, layer = self.get_player_input()

        hit, vessel = self.fire_at(row, col, layer)
        if hit:
            print(f"It's a hit on {vessel.name}!")
            if self.check_for_win(self.get_opponent_board()):
                print(f"Player {self.current_turn} wins!")
                return True
        else:
            print("Miss!")

        self.switch_turn()
        return False

    def play(self):
        game_over = False
        while not game_over:
            game_over = self.take_turn()
        print("Game over!")


def setup_game():
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

